import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from psycopg import Error as PsycopgError

from database import get_db_connection
from errors import register_error_handlers
from schemas import HistoryResponse, StationsResponse, SummaryResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

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
        "http://localhost:4174",
        "http://127.0.0.1:4174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database errors, bad input and unexpected crashes are all turned into
# consistent JSON responses in errors.py, so endpoints don't need try/except.
register_error_handlers(app)


@app.get("/")
def home():
    return {"message": "Welcome to Lahore Smog Forecaster API", "status": "running"}


@app.get("/health")
def health_check():
    """Report whether the API and the database are both reachable."""
    try:
        with get_db_connection() as connection:
            connection.execute("SELECT 1;")
    except (PsycopgError, RuntimeError):
        logging.getLogger("lahore_api").warning("Health check: database unreachable")
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "database": "unavailable"},
        )

    return {"status": "healthy", "database": "connected"}


@app.get("/api/stations", response_model=StationsResponse)
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


@app.get("/api/summary", response_model=SummaryResponse)
def get_summary():
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


@app.get("/api/history/{time_range}", response_model=HistoryResponse)
def get_history(time_range: str):
    # Keep the original API contract: invalid ranges return HTTP 400.
    if time_range not in ("weekly", "monthly", "yearly"):
        raise HTTPException(
            status_code=400,
            detail="Invalid time range. Use weekly, monthly, or yearly.",
        )

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
