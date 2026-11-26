
import sys

import numpy as np
import pandas as pd

# Default horizon is 24 hours
horizon = int(sys.argv[1]) if len(sys.argv) > 1 else 24

if horizon not in [24, 48, 72]:
    raise ValueError("Horizon must be 24, 48, or 72 hours.")

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

TARGET = f"pm25_future_{horizon}h"

for split in ["train", "validation", "test"]:
    input_path = f"ml/data/processed/{split}.csv"
    output_path = (
        f"ml/data/processed/model_{split}_{horizon}h.csv"
    )

    df = pd.read_csv(input_path)

    # Generate cyclical month features
    df["month_sin"] = np.sin(
        2 * np.pi * (df["month"] - 1) / 12
    )

    df["month_cos"] = np.cos(
        2 * np.pi * (df["month"] - 1) / 12
    )

    original_count = len(df)

    model_df = df[FEATURES + [TARGET]].dropna()

    model_df.to_csv(output_path, index=False)

    print(f"\n{split.upper()}")
    print("Original records:", original_count)
    print("Usable records:", len(model_df))
    print("Removed records:", original_count - len(model_df))
    print("Saved:", output_path)

print(f"\n{horizon}-hour model datasets prepared successfully!")
