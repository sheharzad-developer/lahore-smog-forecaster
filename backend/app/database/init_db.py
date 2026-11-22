"""Create the database, the stations table, and load sample data.

Run from the backend folder:

    python -m app.database.init_db

Safe to run more than once: it skips anything that already exists.
"""

import psycopg
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict, make_conninfo

from app.database.connection import DATABASE_URL, get_connection
from app.database.seed_data import SAMPLE_HISTORY, SAMPLE_STATIONS

CREATE_STATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS stations (
    id            SERIAL PRIMARY KEY,
    name          TEXT NOT NULL UNIQUE,
    neighbourhood TEXT NOT NULL,
    pm25          INTEGER NOT NULL CHECK (pm25 >= 0),
    status        TEXT NOT NULL CHECK (status IN ('Online', 'Offline')),
    lat           DOUBLE PRECISION NOT NULL,
    lng           DOUBLE PRECISION NOT NULL
);
"""


CREATE_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS historical_readings (
    id         SERIAL PRIMARY KEY,
    time_range TEXT NOT NULL CHECK (time_range IN ('weekly', 'monthly', 'yearly')),
    label      TEXT NOT NULL,
    pm25       INTEGER NOT NULL CHECK (pm25 >= 0),
    UNIQUE (time_range, label)
);
"""


def create_database_if_missing() -> None:
    """Connect to the default 'postgres' database and create ours if needed."""
    params = conninfo_to_dict(DATABASE_URL)
    db_name = params.get("dbname")
    admin_conninfo = make_conninfo(DATABASE_URL, dbname="postgres")

    with psycopg.connect(admin_conninfo, autocommit=True) as conn:
        exists = conn.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (db_name,)
        ).fetchone()
        if exists:
            print(f"Database '{db_name}' already exists.")
        else:
            conn.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            print(f"Created database '{db_name}'.")


def create_tables_and_seed() -> None:
    with get_connection() as conn:
        conn.execute(CREATE_STATIONS_TABLE)
        conn.execute(CREATE_HISTORY_TABLE)
        seed_stations(conn)
        seed_history(conn)


def seed_history(conn) -> None:
    count = conn.execute(
        "SELECT COUNT(*) AS n FROM historical_readings"
    ).fetchone()["n"]
    if count:
        print(f"Table 'historical_readings' already has {count} rows; not seeding.")
        return

    rows = [
        {"time_range": time_range, "label": label, "pm25": pm25}
        for time_range, readings in SAMPLE_HISTORY.items()
        for label, pm25 in readings
    ]
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO historical_readings (time_range, label, pm25)
            VALUES (%(time_range)s, %(label)s, %(pm25)s)
            """,
            rows,
        )
    print(f"Inserted {len(rows)} historical readings.")


def seed_stations(conn) -> None:
    count = conn.execute("SELECT COUNT(*) AS n FROM stations").fetchone()["n"]
    if count:
        print(f"Table 'stations' already has {count} rows; not seeding.")
        return

    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO stations (name, neighbourhood, pm25, status, lat, lng)
            VALUES (%(name)s, %(neighbourhood)s, %(pm25)s, %(status)s,
                    %(lat)s, %(lng)s)
            """,
            SAMPLE_STATIONS,
        )
    print(f"Inserted {len(SAMPLE_STATIONS)} sample stations.")


if __name__ == "__main__":
    if not DATABASE_URL:
        raise SystemExit(
            "DATABASE_URL is not set. Edit backend/.env first."
        )
    create_database_if_missing()
    create_tables_and_seed()
    print("Database ready.")
