from database import get_connection

try:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT current_database();")
    database_name = cursor.fetchone()[0]

    print("Database:", database_name)

    cursor.execute("SELECT COUNT(*) FROM stations;")
    station_count = cursor.fetchone()[0]

    print("Stations table exists!")
    print("Number of stations:", station_count)

    cursor.close()
    connection.close()

except Exception as error:
    print("Database test failed:")
    print(error)