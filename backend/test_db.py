
from database import get_db_connection


def test_database_connection():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database();")
                database_name = cursor.fetchone()[0]

                print("Database:", database_name)

                cursor.execute("SELECT COUNT(*) FROM stations;")
                station_count = cursor.fetchone()[0]

                print("Stations table exists!")
                print("Number of stations:", station_count)

        print("Database test passed!")

    except Exception as error:
        print("Database test failed:")
        print(error)


if __name__ == "__main__":
    test_database_connection()
