import pandas as pd

df = pd.read_csv("ml/data/raw/gulberg_pm25.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

df["year_month"] = df["timestamp"].dt.strftime("%Y-%m")

monthly = df.groupby("year_month").agg(
    readings=("pm25", "count"),
    mean_pm25=("pm25", "mean"),
    median_pm25=("pm25", "median"),
    max_pm25=("pm25", "max"),
).reset_index()

print("\n========== MONTHLY PM2.5 DISTRIBUTION ==========")
print(monthly.round(2).to_string(index=False))