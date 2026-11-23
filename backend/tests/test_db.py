from database import get_db_connection


def test_database_connection():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database();")
            database_name = cursor.fetchone()[0]

            assert database_name == "lahore_smog"

            cursor.execute("SELECT COUNT(*) FROM stations;")
            station_count = cursor.fetchone()[0]

            assert station_count > 0