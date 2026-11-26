
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "ml/data/raw/gulberg_pm25.csv"


def analyze_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp")

    print("\n========== DATASET OVERVIEW ==========")
    print("Total records:", len(df))
    print("Columns:", df.columns.tolist())

    print("\n========== MISSING VALUES ==========")
    print(df.isnull().sum())

    print("\n========== DUPLICATES ==========")
    print("Duplicate timestamps:", df["timestamp"].duplicated().sum())

    print("\n========== PM2.5 STATISTICS ==========")
    print(df["pm25"].describe())

    print("\n========== INVALID VALUES ==========")
    print("Negative readings:", (df["pm25"] < 0).sum())
    print("Zero readings:", (df["pm25"] == 0).sum())

    # Timestamp gaps
    print("\n========== TIMESTAMP GAPS ==========")

    expected = pd.date_range(
        start=df["timestamp"].min(),
        end=df["timestamp"].max(),
        freq="h",
        tz="UTC",
    )

    missing = expected.difference(df["timestamp"])

    print("Expected hourly records:", len(expected))
    print("Actual records:", len(df))
    print("Missing timestamps:", len(missing))

    # Missing periods by date
    print("\n========== MISSING PERIODS ==========")

    missing_df = pd.DataFrame({"timestamp": missing})
    missing_df["date"] = missing_df["timestamp"].dt.date

    daily_missing = (
        missing_df.groupby("date")
        .size()
        .reset_index(name="missing_hours")
    )

    print("Dates affected:", len(daily_missing))
    print(daily_missing.sort_values(
        "missing_hours", ascending=False
    ).head(15).to_string(index=False))

    # Longest missing gaps
    print("\n========== LONGEST MISSING GAPS ==========")

    missing_series = pd.Series(missing)

    gap_groups = (
        missing_series.diff()
        .ne(pd.Timedelta(hours=1))
        .cumsum()
    )

    gap_periods = (
        missing_series.groupby(gap_groups)
        .agg(
            start="min",
            end="max",
            missing_hours="size"
        )
        .reset_index()
    )

    print(
        gap_periods.sort_values(
            "missing_hours", ascending=False
        ).head(15).to_string(index=False)
    )

    # Zero readings
    print("\n========== ZERO PM2.5 READINGS ==========")

    zero_rows = df[df["pm25"] == 0]

    for _, row in zero_rows.iterrows():
        print("\nZero reading:", row["timestamp"])

        nearby = df[
            (df["timestamp"] >= row["timestamp"] - pd.Timedelta(hours=3))
            & (df["timestamp"] <= row["timestamp"] + pd.Timedelta(hours=3))
        ]

        print(nearby[["timestamp", "pm25"]].to_string(index=False))

    # Extreme readings
    print("\n========== EXTREME PM2.5 READINGS ==========")

    extreme_rows = df[df["pm25"] >= 500]

    print(
        extreme_rows[["timestamp", "pm25"]]
        .sort_values("pm25", ascending=False)
        .to_string(index=False)
    )
    print("\n========== JANUARY POLLUTION EPISODE ==========")

    start_date = "2026-01-17"
    end_date = "2026-01-20"

    episode = df[
        (df["timestamp"] >= start_date)
        & (df["timestamp"] < end_date)
    ]

    print("Total readings:", len(episode))
    print("\nHourly PM2.5 readings:")

    print(
        episode[["timestamp", "pm25"]]
        .to_string(index=False)
    )

    print("\nEpisode statistics:")
    print(episode["pm25"].describe())


    plt.figure(figsize=(14, 6))

    plt.plot(
        episode["timestamp"],
        episode["pm25"],
        marker="o",
        markersize=3,
    )

    plt.title("Gulberg III PM2.5 - January 17–19, 2026")
    plt.xlabel("Date (UTC)")
    plt.ylabel("PM2.5 (µg/m³)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("ml/data/processed/january_episode.png")
    plt.show()

    # May 2, 2026 pollution event
    print("\n========== MAY 2, 2026 POLLUTION EVENT ==========")

    may_event = df[
        df["timestamp"].dt.date == pd.Timestamp("2026-05-02").date()
    ]

    print(may_event[["timestamp", "pm25"]].to_string(index=False))
    print("\nMay statistics:")
    print(may_event["pm25"].describe())

    plt.figure(figsize=(14, 6))
    plt.plot(
        may_event["timestamp"],
        may_event["pm25"],
        marker="o",
        markersize=4,
    )

    plt.title("Gulberg III PM2.5 - May 2, 2026")
    plt.xlabel("Time (UTC)")
    plt.ylabel("PM2.5 (µg/m³)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("ml/data/processed/may_2_2026.png")
    plt.show()

    # September 18, 2026 pollution event
    print("\n========== SEPTEMBER 18, 2026 POLLUTION EVENT ==========")

    september_event = df[
        df["timestamp"].dt.date == pd.Timestamp("2026-09-18").date()
    ]

    print(
        september_event[["timestamp", "pm25"]].to_string(index=False)
    )
    print("\nSeptember statistics:")
    print(september_event["pm25"].describe())

    plt.figure(figsize=(14, 6))
    plt.plot(
        september_event["timestamp"],
        september_event["pm25"],
        marker="o",
        markersize=4,
    )

    plt.title("Gulberg III PM2.5 - September 18, 2026")
    plt.xlabel("Time (UTC)")
    plt.ylabel("PM2.5 (µg/m³)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("ml/data/processed/september_18_2026.png")
    plt.show()


if __name__ == "__main__":
    analyze_data()
