
import os
import sys
import joblib
import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

horizon = int(sys.argv[1]) if len(sys.argv) > 1 else 24

if horizon not in [24, 48, 72]:
    raise ValueError("Horizon must be 24, 48, or 72 hours.")

TARGET = f"pm25_future_{horizon}h"

test = pd.read_csv(
    f"ml/data/processed/model_test_{horizon}h.csv"
)

model_path = f"ml/models/gradient_boosting_{horizon}h_tuned.pkl"
model = joblib.load(model_path)

X_test = test.drop(columns=[TARGET])
y_test = test[TARGET]

# Model predictions
model_predictions = model.predict(X_test)

# Persistence baseline: current PM2.5
baseline_predictions = test["pm25"]

# Evaluate both on exactly the same rows
results = {
    "Gradient Boosting": model_predictions,
    "Persistence Baseline": baseline_predictions
}

print(f"\n========== {horizon}-HOUR FINAL TEST RESULTS ==========")

for name, predictions in results.items():
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print(f"\n{name}")
    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R²:", round(r2, 4))

model_mae = mean_absolute_error(y_test, model_predictions)
baseline_mae = mean_absolute_error(y_test, baseline_predictions)

improvement = (
    (baseline_mae - model_mae) / baseline_mae
) * 100

print("\nMAE improvement:", round(improvement, 2), "%")
print("Test samples:", len(test))
