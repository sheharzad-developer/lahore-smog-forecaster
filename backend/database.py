"""Database connection for the API and scripts in backend/.

Returns a standard psycopg connection whose rows are tuples, so
`row[0]` / `cursor.fetchone()[0]` work. Use it in a `with` block so the
connection is committed and closed automatically:

    with get_db_connection() as connection:
        ...

Reads DATABASE_URL from backend/.env.
"""

import psycopg

from app.database.connection import DATABASE_URL


def get_db_connection() -> psycopg.Connection:
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Add it to backend/.env."
        )
    return psycopg.connect(DATABASE_URL)


# Older name, still used by test_db.py.
get_connection = get_db_connection
