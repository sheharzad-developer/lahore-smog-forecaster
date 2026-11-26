import pandas as pd

INPUT_PATH = "ml/data/processed/gulberg_pm25_features.csv"
OUTPUT_DIR = "ml/data/processed"

FORECAST_GAP_HOURS = 72


def split_data():
    df = pd.read_csv(INPUT_PATH)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True
    )

    df = df.sort_values("timestamp").reset_index(drop=True)

    # Calculate chronological boundaries
    train_boundary = int(len(df) * 0.70)
    validation_boundary = int(len(df) * 0.85)

    train_end = df.loc[train_boundary - 1, "timestamp"]
    validation_start = (
        df.loc[train_boundary, "timestamp"]
        + pd.Timedelta(hours=FORECAST_GAP_HOURS)
    )

    validation_end = df.loc[
        validation_boundary - 1, "timestamp"
    ]

    test_start = (
        df.loc[validation_boundary, "timestamp"]
        + pd.Timedelta(hours=FORECAST_GAP_HOURS)
    )

    # Split chronologically with a 72-hour gap
    train = df[df["timestamp"] <= train_end].copy()

    validation = df[
        (df["timestamp"] >= validation_start)
        & (df["timestamp"] <= validation_end)
    ].copy()

    test = df[df["timestamp"] >= test_start].copy()

    # Save datasets
    train.to_csv(f"{OUTPUT_DIR}/train.csv", index=False)
    validation.to_csv(
        f"{OUTPUT_DIR}/validation.csv", index=False
    )
    test.to_csv(f"{OUTPUT_DIR}/test.csv", index=False)

    print("========== DATASET SPLIT ==========")
    print("Original records:", len(df))
    print("Training records:", len(train))
    print("Validation records:", len(validation))
    print("Testing records:", len(test))

    print("\nTraining range:")
    print(train["timestamp"].min(), "to", train["timestamp"].max())

    print("\nValidation range:")
    print(
        validation["timestamp"].min(),
        "to",
        validation["timestamp"].max()
    )

    print("\nTesting range:")
    print(test["timestamp"].min(), "to", test["timestamp"].max())


if __name__ == "__main__":
    split_data()