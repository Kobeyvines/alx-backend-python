#!/usr/bin/python3

seed = __import__('seed')

# Connect to MySQL server
connection = seed.connect_db()
if connection:
    seed.create_database(connection)
    connection.close()
    print("Connection successful")

    # Connect to ALX_prodev database
    connection = seed.connect_to_prodev()

    if connection:
        seed.create_table(connection)
        seed.insert_data(connection, 'user_data.csv')

        cursor = connection.cursor()

        # Check if database exists
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("Database ALX_prodev is present")

        # Print first 5 rows from user_data
        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)

        cursor.close()
        connection.close()
