
from pathlib import Path

import joblib
import pandas as pd
import numpy as np

from datetime import timedelta


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "ml" / "models"

# Oldest latest-reading we still forecast from. OpenAQ often publishes
# Gulberg readings several hours late (5h observed), and 24-72h forecasts
# stay meaningful with a reading a few hours old.
MAX_DATA_AGE_HOURS = 6

# Exact feature order used during model training
FEATURES = [
    "pm25",
    "pm25_lag_1",
    "pm25_lag_3",
    "pm25_lag_6",
    "pm25_lag_24",
    "pm25_rolling_3h",
    "pm25_rolling_6h",
    "pm25_rolling_24h",
    "hour_sin",
    "hour_cos",
    "day_of_week_sin",
    "day_of_week_cos",
    "month_sin",
    "month_cos",
]


def load_models():
    """Load all forecasting models."""
    models = {}

    for horizon in [24, 48, 72]:
        model_path = (
            MODEL_DIR / f"gradient_boosting_{horizon}h_tuned.pkl"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )

        models[horizon] = joblib.load(model_path)

        if list(models[horizon].feature_names_in_) != FEATURES:
            raise ValueError(
                f"Feature mismatch in {horizon}-hour model."
            )

    return models


# Load models once when this module is imported
MODELS = load_models()


def predict(features: pd.DataFrame) -> dict:
    """Generate predictions for all three forecasting horizons."""

    if list(features.columns) != FEATURES:
        raise ValueError(
            "Input features do not match the expected feature names and order."
        )

    if len(features) != 1:
        raise ValueError(
            "Prediction requires exactly one row of features."
        )

    if features.isna().any().any():
        raise ValueError("Input features contain missing values.")

    predictions = {}

    for horizon, model in MODELS.items():
        prediction = model.predict(features)[0]

        predictions[f"{horizon}h"] = round(
            max(0.0, float(prediction)), 2
        )

    return predictions


def prepare_latest_features(readings: pd.DataFrame) -> tuple[pd.DataFrame, pd.Timestamp]:
    """
    Prepare the latest valid row of historical PM2.5 readings
    using the same feature calculations as model training.

    Expected columns: timestamp, pm25
    """

    required_columns = {"timestamp", "pm25"}

    if not required_columns.issubset(readings.columns):
        raise ValueError("Readings must contain timestamp and pm25 columns.")

    df = readings[["timestamp", "pm25"]].copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], utc=True, errors="coerce"
    )

    df["pm25"] = pd.to_numeric(df["pm25"], errors="coerce")

    if df.isna().any().any():
        raise ValueError("Readings contain invalid timestamps or PM2.5 values.")

    if (df["pm25"] < 0).any():
        raise ValueError("PM2.5 readings cannot be negative.")

    df = df.sort_values("timestamp").reset_index(drop=True)

    if df["timestamp"].duplicated().any():
        raise ValueError("Duplicate timestamps found in readings.")

    df = df.set_index("timestamp")

    # Latest reading timestamp
    latest_timestamp = df.index.max()

    # Exact historical lag features
    features = {"pm25": df.loc[latest_timestamp, "pm25"]}

    for lag in [1, 3, 6, 24]:
        historical_timestamp = latest_timestamp - pd.Timedelta(hours=lag)

        if historical_timestamp not in df.index:
            raise ValueError(
                f"Missing reading for lag of {lag} hours."
            )

        features[f"pm25_lag_{lag}"] = df.loc[
            historical_timestamp, "pm25"
        ]

    # Rolling averages using the previous complete hourly windows
    for window in [3, 6, 24]:
        timestamps = pd.date_range(
            end=latest_timestamp - pd.Timedelta(hours=1),
            periods=window,
            freq="h",
            tz="UTC",
        )

        if not timestamps.isin(df.index).all():
            raise ValueError(
                f"Incomplete historical data for {window}-hour rolling average."
            )

        features[f"pm25_rolling_{window}h"] = (
            df.loc[timestamps, "pm25"].mean()
        )

    # Lahore local calendar features
    local_timestamp = latest_timestamp.tz_convert("Asia/Karachi")

    hour = local_timestamp.hour
    day_of_week = local_timestamp.day_of_week
    month = local_timestamp.month

    features["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    features["hour_cos"] = np.cos(2 * np.pi * hour / 24)

    features["day_of_week_sin"] = np.sin(
        2 * np.pi * day_of_week / 7
    )
    features["day_of_week_cos"] = np.cos(
        2 * np.pi * day_of_week / 7
    )

    features["month_sin"] = np.sin(
        2 * np.pi * (month - 1) / 12
    )
    features["month_cos"] = np.cos(
        2 * np.pi * (month - 1) / 12
    )

    feature_df = pd.DataFrame([features], columns=FEATURES)

    # Refuse to build features from outdated readings
    validate_data_freshness(latest_timestamp)

    return feature_df, latest_timestamp

def validate_data_freshness(
    latest_timestamp: pd.Timestamp,
    max_age_hours: int = MAX_DATA_AGE_HOURS,
) -> None:
    """Reject readings that are too old for forecasting."""

    now = pd.Timestamp.now(tz="UTC")
    age = now - latest_timestamp

    if age > timedelta(hours=max_age_hours):
        age_hours = age.total_seconds() / 3600
        raise ValueError(
            f"Latest reading is stale ({age_hours:.1f} hours old, "
            f"from {latest_timestamp:%Y-%m-%d %H:%M} UTC). "
            f"Maximum allowed age: {max_age_hours} hours."
        )