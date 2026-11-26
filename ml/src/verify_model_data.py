
import sys
import numpy as np
import pandas as pd

horizon = int(sys.argv[1]) if len(sys.argv) > 1 else 24

if horizon not in [24, 48, 72]:
    raise ValueError("Horizon must be 24, 48, or 72.")

for split in ["train", "validation", "test"]:
    path = f"ml/data/processed/model_{split}_{horizon}h.csv"
    df = pd.read_csv(path)

    print(f"\n========== {split.upper()} ==========")
    print("Shape:", df.shape)
    print("Missing values:", df.isna().sum().sum())
    print(
        "Infinite values:",
        np.isinf(df.select_dtypes(include="number")).sum().sum()
    )
    print(
        "Target:",
        f"pm25_future_{horizon}h" in df.columns
    )
    print("Features:", len(df.columns) - 1)
