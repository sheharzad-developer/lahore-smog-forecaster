"""PostgreSQL connection helpers.

Settings come from backend/.env (see .env.example), never from source code.
"""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection() -> psycopg.Connection:
    """Open a connection that returns rows as dictionaries."""
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy backend/.env.example to "
            "backend/.env and fill in your PostgreSQL password."
        )
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)
