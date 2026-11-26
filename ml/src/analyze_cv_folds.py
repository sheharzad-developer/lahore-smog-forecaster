import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

df = pd.read_csv("ml/data/processed/model_train_24h.csv")

X = df.drop(columns=["pm25_future_24h"])
y = df["pm25_future_24h"]

tscv = TimeSeriesSplit(
    n_splits=3,
    gap=72
)

for fold, (train_idx, val_idx) in enumerate(tscv.split(X), start=1):
    y_train = y.iloc[train_idx]
    y_val = y.iloc[val_idx]

    print(f"\n========== FOLD {fold} ==========")
    print("Training samples:", len(train_idx))
    print("Validation samples:", len(val_idx))
    print("Training target mean:", round(y_train.mean(), 2))
    print("Validation target mean:", round(y_val.mean(), 2))
    print("Training target median:", round(y_train.median(), 2))
    print("Validation target median:", round(y_val.median(), 2))