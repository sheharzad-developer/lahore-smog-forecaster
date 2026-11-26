import sys
import pandas as pd

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

horizon = int(sys.argv[1]) if len(sys.argv) > 1 else 24

if horizon not in [24, 48, 72]:
    raise ValueError("Horizon must be 24, 48, or 72.")

df = pd.read_csv(
    f"ml/data/processed/model_validation_{horizon}h.csv"
)

actual = df[f"pm25_future_{horizon}h"]
predicted = df["pm25"]

print(f"========== {horizon}-HOUR PERSISTENCE BASELINE ==========")
print("MAE:", round(mean_absolute_error(actual, predicted), 2))
print("RMSE:", round(np.sqrt(mean_squared_error(actual, predicted)), 2))
print("R²:", round(r2_score(actual, predicted), 4))
