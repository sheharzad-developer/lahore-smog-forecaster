import pandas as pd
import numpy as np
import joblib
import os

from sklearn.ensemble import HistGradientBoostingRegressor
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

model = HistGradientBoostingRegressor(
    max_iter=200,
    max_leaf_nodes=15,
    learning_rate=0.05,
    min_samples_leaf=20,
    l2_regularization=1.0,
    random_state=42,
)

print("Training Gradient Boosting...")

model.fit(X_train, y_train)

predictions = model.predict(X_validation)

mae = mean_absolute_error(y_validation, predictions)
rmse = np.sqrt(mean_squared_error(y_validation, predictions))
r2 = r2_score(y_validation, predictions)

print("\n========== GRADIENT BOOSTING RESULTS ==========")
print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²:   {r2:.4f}")

os.makedirs("ml/models", exist_ok=True)

joblib.dump(
    model,
    "ml/models/gradient_boosting_24h.pkl"
)

print("\nModel saved: ml/models/gradient_boosting_24h.pkl")