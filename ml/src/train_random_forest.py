import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

TRAIN_PATH = "ml/data/processed/model_train_24h.csv"
VALIDATION_PATH = "ml/data/processed/model_validation_24h.csv"

TARGET = "pm25_future_24h"

train = pd.read_csv(TRAIN_PATH)
validation = pd.read_csv(VALIDATION_PATH)

X_train = train.drop(columns=[TARGET])
y_train = train[TARGET]

X_validation = validation.drop(columns=[TARGET])
y_validation = validation[TARGET]

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
)

print("Training Random Forest...")

model.fit(X_train, y_train)

predictions = model.predict(X_validation)

comparison = pd.DataFrame({
    "actual": y_validation,
    "predicted": predictions,
    "current_pm25": X_validation["pm25"],
})

comparison["error"] = (
    comparison["actual"] - comparison["predicted"]
)

print("\n========== SAMPLE PREDICTIONS ==========")
print(comparison.head(10).round(2).to_string(index=False))

print("\n========== ERROR ANALYSIS ==========")
print("Mean actual:", round(comparison["actual"].mean(), 2))
print("Mean predicted:", round(comparison["predicted"].mean(), 2))
print("Mean error:", round(comparison["error"].mean(), 2))
print("Maximum absolute error:", round(comparison["error"].abs().max(), 2))

mae = mean_absolute_error(y_validation, predictions)
rmse = np.sqrt(mean_squared_error(y_validation, predictions))
r2 = r2_score(y_validation, predictions)

print("\n========== RANDOM FOREST RESULTS ==========")
print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²:   {r2:.4f}")

print("\n========== FEATURE IMPORTANCE ==========")

importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": model.feature_importances_,
})

importance = importance.sort_values(
    by="importance",
    ascending=False,
)

print(importance.to_string(index=False))

comparison["pm25_category"] = pd.cut(
    comparison["current_pm25"],
    bins=[-float("inf"), 35, 75, 150, float("inf")],
    labels=["Low", "Moderate", "High", "Very High"],
)

print("\n========== ERROR BY CURRENT PM2.5 LEVEL ==========")

category_results = comparison.groupby(
    "pm25_category",
    observed=False
).agg(
    samples=("actual", "count"),
    actual_mean=("actual", "mean"),
    predicted_mean=("predicted", "mean"),
    mae=("error", lambda x: x.abs().mean()),
    mean_error=("error", "mean"),
)

print(category_results.round(2))