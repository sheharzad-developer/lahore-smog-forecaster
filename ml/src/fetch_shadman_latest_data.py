"""Fetch the most recent PM2.5 readings for live forecasting.

Saves to a separate file so the historical training dataset
(ml/data/raw/gulberg_pm25.csv) is never modified.

Run from the project root:

    python ml/src/fetch_latest_data.py
"""

import logging
from pathlib import Path

import pandas as pd
import requests

from collect_data import BASE_URL, OPENAQ_API_KEY

SENSOR_ID = 14671499
OUTPUT_PATH = Path("ml/data/raw/shadman_pm25_latest.csv")

LOG_PATH = Path("logs/collector.log")

logging.basicConfig(
    filename="logs/collector-error.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
)

# Forecasting needs the latest reading plus the previous 24 hours
# (lag_24 and the 24-hour rolling average). 72 hours leaves room for gaps.
HOURS_TO_FETCH = 72

# Matches MAX_DATA_AGE_HOURS in backend/services/prediction_service.py
MAX_DATA_AGE_HOURS = 6


def fetch_latest_data():
    if not OPENAQ_API_KEY:
        raise ValueError("OPENAQ_API_KEY is missing from ml/.env")

    now = pd.Timestamp.now(tz="UTC")
    request_end = now.floor("h")
    start = request_end - pd.Timedelta(hours=HOURS_TO_FETCH)

    response = requests.get(
        f"{BASE_URL}/sensors/{SENSOR_ID}/hours",
        headers={"X-API-Key": OPENAQ_API_KEY},
        params={
            "datetime_from": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "datetime_to": request_end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "limit": 1000,
            "page": 1,
        },
        timeout=30,
    )
    response.raise_for_status()

    results = response.json().get("results", [])

    if not results:
        raise ValueError(
            f"OpenAQ returned no readings between {start} and {now}."
        )

    df = pd.DataFrame({
        "timestamp": [r["period"]["datetimeFrom"]["utc"] for r in results],
        "pm25": [r["value"] for r in results],
        "sensor_id": SENSOR_ID,
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.drop_duplicates(subset=["timestamp"]).sort_values("timestamp")

    latest = df["timestamp"].max()

    # Reject data that is too old. `now` is the real current time (not
    # hour-rounded), so this matches the API's freshness check exactly.
    age = now - latest

    latest = df["timestamp"].max()
    print(f"OpenAQ latest timestamp: {latest}")
    age = now - latest

    if age > pd.Timedelta(hours=MAX_DATA_AGE_HOURS):
        raise ValueError(
            f"OpenAQ returned stale data. Latest reading is "
            f"{age.total_seconds() / 3600:.1f} hours old. "
            f"Maximum allowed age: {MAX_DATA_AGE_HOURS} hours."
        )

    # Never replace newer stored data with older data.
    if OUTPUT_PATH.exists():
        existing = pd.read_csv(OUTPUT_PATH, parse_dates=["timestamp"])
        existing["timestamp"] = pd.to_datetime(
            existing["timestamp"], utc=True
        )

        existing_latest = existing["timestamp"].max()

        if latest < existing_latest:
            raise ValueError(
                f"Incoming data is older than stored data. "
                f"Incoming: {latest}, stored: {existing_latest}."
            )

    # Write to a temporary file first, then swap it in. The API never sees
    # a half-written CSV, and a failed write leaves the old file intact.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = OUTPUT_PATH.with_suffix(".tmp")
    df.to_csv(temp_path, index=False)
    temp_path.replace(OUTPUT_PATH)

    expected = pd.date_range(df["timestamp"].min(), latest, freq="h")
    missing = len(expected.difference(df["timestamp"]))

    print(f"Saved {len(df)} readings to {OUTPUT_PATH}")
    print(f"Range: {df['timestamp'].min()} to {latest}")
    print(f"Missing hours in range: {missing}")
    print(f"Latest reading age: {now - latest} (at {now})")

    return df


if __name__ == "__main__":
    try:
        fetch_latest_data()
    except Exception:
        logging.exception("OpenAQ data collection failed")
        raise