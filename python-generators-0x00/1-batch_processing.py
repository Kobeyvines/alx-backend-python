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

# Generator: fetch users in batches
def stream_users_in_batches(batch_size):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch  # yield the batch

    cursor.close()
    connection.close()

# Process each batch to filter users over age 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):  # loop 1
        filtered_batch = [user for user in batch if user[3] > 25]  # loop 2 is hidden inside list comprehension
        yield filtered_batch

# Test run (for your learning; comment out before submission if required)
if __name__ == "__main__":
    for filtered in batch_processing(2):  # loop 3 here
        print(filtered)
