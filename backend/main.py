import psycopg
from fastapi import FastAPI, HTTPException
from psycopg import Error as PsycopgError
from fastapi.middleware.cors import CORSMiddleware
from schemas import StationsResponse, SummaryResponse, HistoryResponse

from app.database.connection import get_connection

from database import get_db_connection

app = FastAPI(
    title="Lahore Smog Forecaster API",
    description="Backend API for Lahore air quality monitoring",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to Lahore Smog Forecaster API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


STATION_COLUMNS = "id, name, neighbourhood, pm25, status, lat, lng"


def fetch_stations() -> list[dict]:
    """Load every station from PostgreSQL, ordered by id."""
    try:
        with get_connection() as conn:
            return conn.execute(
                f"SELECT {STATION_COLUMNS} FROM stations ORDER BY id"
            ).fetchall()
    except (psycopg.Error, RuntimeError) as exc:
        print(f"Database error: {exc}")
        raise HTTPException(
            status_code=503,
            detail="Station database is unavailable.",
        ) from exc


@app.get("/api/stations", response_model=StationsResponse)
def get_stations():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT id, name, neighbourhood, pm25, status, lat, lng
                FROM stations
                ORDER BY id;
            """)

            rows = cursor.fetchall()
            cursor.close()

        stations_data = [
            {
                "id": row[0],
                "name": row[1],
                "neighbourhood": row[2],
                "pm25": row[3],
                "status": row[4],
                "lat": row[5],
                "lng": row[6],
            }
            for row in rows
        ]

        return {
            "data_type": "database",
            "count": len(stations_data),
            "stations": stations_data,
        }

    except PsycopgError:
        raise HTTPException(
            status_code=503, detail="Database is temporarily unavailable."
        )


@app.get("/api/summary", response_model=SummaryResponse)
def get_summary():
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*),
                    COUNT(*) FILTER (WHERE status = 'Online'),
                    COUNT(*) FILTER (WHERE status = 'Offline'),
                    COALESCE(ROUND(AVG(pm25)::numeric, 2), 0)
                FROM stations;
            """)

            row = cursor.fetchone()
            cursor.close()

        return {
            "data_type": "database",
            "total_stations": row[0],
            "online_stations": row[1],
            "offline_stations": row[2],
            "average_pm25": float(row[3]),
        }

    except PsycopgError:
        raise HTTPException(
            status_code=503, detail="Database is temporarily unavailable."
        )


@app.get("/api/history/{time_range}", response_model=HistoryResponse)
def get_history(time_range: str):
    if time_range not in ["weekly", "monthly", "yearly"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid time range. Use weekly, monthly, or yearly.",
        )

    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT label, pm25
                FROM historical_readings
                WHERE time_range = %s
                ORDER BY id;
            """,
                (time_range,),
            )

            rows = cursor.fetchall()
            cursor.close()

        readings = [{"day": row[0], "pm25": row[1]} for row in rows]

        return {
            "data_type": "database",
            "time_range": time_range,
            "count": len(readings),
            "readings": readings,
        }

    except PsycopgError:
        raise HTTPException(
            status_code=503, detail="Database is temporarily unavailable."
        )


@app.get("/api/stations")
def get_stations():
    with get_db_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, neighbourhood, pm25, status, lat, lng
            FROM stations
            ORDER BY id;
        """)

        rows = cursor.fetchall()
        cursor.close()

    stations_data = [
        {
            "id": row[0],
            "name": row[1],
            "neighbourhood": row[2],
            "pm25": row[3],
            "status": row[4],
            "lat": row[5],
            "lng": row[6],
        }
        for row in rows
    ]

    return {
        "data_type": "database",
        "count": len(stations_data),
        "stations": stations_data,
    }
