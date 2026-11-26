
import os
import sys

import joblib
import pandas as pd
import numpy as np

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Read forecasting horizon (default: 24 hours)
horizon = int(sys.argv[1]) if len(sys.argv) > 1 else 24

if horizon not in [24, 48, 72]:
    raise ValueError("Horizon must be 24, 48, or 72 hours.")

print(f"Forecasting horizon: {horizon} hours")

# Load matching datasets
train = pd.read_csv(
    f"ml/data/processed/model_train_{horizon}h.csv"
)

validation = pd.read_csv(
    f"ml/data/processed/model_validation_{horizon}h.csv"
)

TARGET = f"pm25_future_{horizon}h"

X_train = train.drop(columns=[TARGET])
y_train = train[TARGET]

X_validation = validation.drop(columns=[TARGET])
y_validation = validation[TARGET]

# Model
model = HistGradientBoostingRegressor(random_state=42)

# Hyperparameter search space
param_distributions = {
    "max_iter": [100, 200, 300, 400],
    "learning_rate": [0.01, 0.03, 0.05, 0.1],
    "max_leaf_nodes": [7, 15, 20, 31],
    "min_samples_leaf": [10, 20, 30, 50],
    "l2_regularization": [0.0, 0.1, 1.0, 5.0, 10.0],
}

# Chronological cross-validation with 72-hour gap
time_split = TimeSeriesSplit(
    n_splits=3,
    gap=72
)

search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_distributions,
    n_iter=20,
    scoring="neg_mean_absolute_error",
    cv=time_split,
    random_state=42,
    n_jobs=-1,
    verbose=1,
)

print("\nStarting hyperparameter tuning...")

search.fit(X_train, y_train)

print("\n========== BEST PARAMETERS ==========")
print(search.best_params_)

print("\nBest cross-validation MAE:", -search.best_score_)

best_model = search.best_estimator_

# Validation evaluation
predictions = best_model.predict(X_validation)

print("\n========== VALIDATION RESULTS ==========")
print("MAE:", round(mean_absolute_error(y_validation, predictions), 2))
print("RMSE:", round(np.sqrt(mean_squared_error(y_validation, predictions)), 2))
print("R²:", round(r2_score(y_validation, predictions), 4))

# Save horizon-specific model
os.makedirs("ml/models", exist_ok=True)

model_path = f"ml/models/gradient_boosting_{horizon}h_tuned.pkl"

joblib.dump(best_model, model_path)

print(f"\n{horizon}-hour model saved successfully!")
print("Model path:", model_path)
