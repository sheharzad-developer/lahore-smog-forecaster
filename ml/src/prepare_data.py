
import pandas as pd

RAW_DATA_PATH = "ml/data/raw/gulberg_pm25.csv"
OUTPUT_PATH = "ml/data/processed/gulberg_pm25_features.csv"

# Hours back for each lag feature: pm25_lag_1, pm25_lag_3, pm25_lag_6, pm25_lag_24
LAG_HOURS = [1, 3, 6, 24]


def prepare_data():
    df = pd.read_csv(RAW_DATA_PATH)

    # Parse timestamps as UTC
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )

    # Sort records chronologically
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Convert UTC timestamps to Lahore local time
    df["timestamp_local"] = df["timestamp"].dt.tz_convert(
        "Asia/Karachi"
    )

    # Extract time-based features
    df["hour"] = df["timestamp_local"].dt.hour
    df["day"] = df["timestamp_local"].dt.day
    df["month"] = df["timestamp_local"].dt.month
    df["day_of_week"] = df["timestamp_local"].dt.day_of_week
    df["is_weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)

    # Create lag features using exact timestamps.
    # (Not shift(): the data has missing hours, so the previous row
    # isn't always the previous hour.)
    for lag in LAG_HOURS:
        lag_df = df[["timestamp", "pm25"]].copy()

        # Move each historical timestamp forward
        lag_df["timestamp"] += pd.Timedelta(hours=lag)

        lag_df = lag_df.rename(
            columns={"pm25": f"pm25_lag_{lag}"}
        )

        # Match the historical reading to the current timestamp
        df = df.merge(
            lag_df,
            on="timestamp",
            how="left"
        )

    lag_columns = [f"pm25_lag_{hours}" for hours in LAG_HOURS]
    original_count = len(df)

    print("========== LAG FEATURES ==========")
    print("Rows missing each lag (earlier hour not in the data):")
    print(df[lag_columns].isna().sum().to_string())

    # A model can't train on rows with missing inputs, so drop them.
    # df = df.dropna(subset=lag_columns).reset_index(drop=True)

    # Create rolling-average features using past readings only
    for window in [3, 6, 24]:
        rolling_df = df[["timestamp", "pm25"]].copy()

        # Shift timestamps forward so historical values align
        # with the time at which they will be used
        rolling_df["timestamp"] += pd.Timedelta(hours=1)

        # Calculate rolling average on a complete hourly timeline
        rolling_df = rolling_df.set_index("timestamp")

        hourly_index = pd.date_range(
            start=rolling_df.index.min(),
            end=rolling_df.index.max(),
            freq="h",
            tz="UTC"
        )

        hourly_df = rolling_df.reindex(hourly_index)

        # Compute on the full hourly timeline (missing hours are NaN), so a
        # window always covers exactly `window` real hours.
        hourly_df[f"pm25_rolling_{window}h"] = (
            hourly_df["pm25"]
            .rolling(window=window, min_periods=window)
            .mean()
        )

        rolling_df = (
            hourly_df[[f"pm25_rolling_{window}h"]]
            .rename_axis("timestamp")
            .reset_index()
        )

        df = df.merge(
            rolling_df,
            on="timestamp",
            how="left"
        )
    # Cyclical time features
    import numpy as np

    df["hour_sin"] = np.sin(
        2 * np.pi * df["hour"] / 24
    )

    df["hour_cos"] = np.cos(
        2 * np.pi * df["hour"] / 24
    )

    df["day_of_week_sin"] = np.sin(
        2 * np.pi * df["day_of_week"] / 7
    )

    df["day_of_week_cos"] = np.cos(
        2 * np.pi * df["day_of_week"] / 7
    )

        # Create future forecasting targets
    FORECAST_HORIZONS = [24, 48, 72]

    for horizon in FORECAST_HORIZONS:
        future_df = df[["timestamp", "pm25"]].copy()

        # Align future readings with the current timestamp
        future_df["timestamp"] -= pd.Timedelta(hours=horizon)

        future_df = future_df.rename(
            columns={"pm25": f"pm25_future_{horizon}h"}
        )

        df = df.merge(
            future_df,
            on="timestamp",
            how="left"
        )

    target_columns = [
        f"pm25_future_{hours}h"
        for hours in FORECAST_HORIZONS
    ]

    print("\n========== FORECAST TARGETS ==========")
    print(df[target_columns].isna().sum().to_string())

    # Save a separate processed dataset
    df.to_csv(OUTPUT_PATH, index=False)

    print("\n========== DATA PREPARATION ==========")
    print("Original records:", original_count)
    print("Processed records:", len(df))
    print("Columns:", df.columns.tolist())

    print("\nFirst five records:")
    print(df.head().to_string(index=False))

    print("\nSaved processed dataset:", OUTPUT_PATH)


if __name__ == "__main__":
    prepare_data()
