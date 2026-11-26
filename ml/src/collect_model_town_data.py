
import os

import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv("ml/.env")

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY")

BASE_URL = "https://api.openaq.org/v3"

# Lahore city center
LAHORE_COORDINATES = "31.5204,74.3587"
SEARCH_RADIUS = 25000


def get_lahore_stations():
    if not OPENAQ_API_KEY:
        raise ValueError("OPENAQ_API_KEY is missing from ml/.env")

    url = f"{BASE_URL}/locations"

    headers = {
        "X-API-Key": OPENAQ_API_KEY
    }

    params = {
        "coordinates": LAHORE_COORDINATES,
        "radius": SEARCH_RADIUS,
        "parameters_id": 2,
        "limit": 1000,
        "page": 1,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    stations = data.get("results", [])

    print(f"Found {len(stations)} monitoring stations.")

    for station in stations:
        print(
            f"ID: {station['id']} | "
            f"Name: {station['name']}"
        )

    return stations

def inspect_location_sensors(location_id):
    url = f"{BASE_URL}/locations/{location_id}/sensors"

    headers = {
        "X-API-Key": OPENAQ_API_KEY
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    sensors = response.json().get("results", [])

    print(f"\nFound {len(sensors)} sensors.")

    for sensor in sensors:
        parameter = sensor.get("parameter", {})

        print({
            "sensor_id": sensor.get("id"),
            "parameter": parameter.get("name"),
            "units": parameter.get("units"),
            "first_measurement": sensor.get("datetimeFirst"),
            "last_measurement": sensor.get("datetimeLast"),
        })

    return sensors

def get_sensor_measurements(sensor_id):
    url = f"{BASE_URL}/sensors/{sensor_id}/hours"

    headers = {
        "X-API-Key": OPENAQ_API_KEY
    }

    all_measurements = []
    page = 1
    limit = 1000

    while True:
        params = {
            "datetime_from": "2025-06-04T00:00:00Z",
            "datetime_to": "2026-11-24T00:00:00Z",
            "limit": limit,
            "page": page,
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        measurements = response.json().get("results", [])

        all_measurements.extend(measurements)

        print(
            f"Page {page}: {len(measurements)} records "
            f"| Total: {len(all_measurements)}"
        )

        if len(measurements) < limit:
            break

        page += 1

    print(f"\nTotal records collected: {len(all_measurements)}")

    rows = []

    for item in all_measurements:
        rows.append({
            "timestamp": item["period"]["datetimeFrom"]["utc"],
            "pm25": item["value"],
            "sensor_id": sensor_id,
        })

    df = pd.DataFrame(rows)

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)

    df = df.drop_duplicates(subset=["timestamp"])
    df = df.sort_values("timestamp")

    output_path = "ml/data/raw/model_town_pm25.csv"

    df.to_csv(output_path, index=False)

    print(f"\nSaved {len(df)} records to {output_path}")
    print(df.head())
    print(df.tail())

    return df

if __name__ == "__main__":
    inspect_location_sensors(6135507)
    get_sensor_measurements(14686635)
