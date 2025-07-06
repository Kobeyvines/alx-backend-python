#!/usr/bin/env python3
import mysql.connector

# 🔧 Connect to the ALX_prodev database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="strong_password",
        database="ALX_prodev"
    )
    
# Generator: yield ages one by one
def stream_user_ages():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # loop 1
        yield row[0]

    cursor.close()
    connection.close()

# Calculate average using the generator
def calculate_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():  # loop 2
        total_age += age
        count += 1

    if count == 0:
        average = 0
    else:
        average = total_age / count

    print(f"Average age of users: {average}")
