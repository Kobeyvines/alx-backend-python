
#!/usr/bin/env python3

import mysql.connector
import csv
import uuid

# connect to mysql server
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
        
    )

#create database alx_prodev if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXITS ALX_prodev")
    connection.commit()
    cursor.close()
    
#connection to the ALX_prodev database
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="",
        database="ALX_prodev"
    )
    
# 🔧 Create table user_data if it doesn't exist
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        )
    """)
    connection.commit()
    cursor.close()

#Insert data into table if it does not already exist (by email uniqueness check)
def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        name, email, age = row
        cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
        result = cursor.fetchone()
        if not result:
            user_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, age))
    connection.commit()
    cursor.close()

#Main seeding logic
if __name__ == "__main__":
    # Connect to server and create database
    conn = connect_db()
    create_database(conn)
    conn.close()

    # Connect to ALX_prodev database and create table
    db_conn = connect_to_prodev()
    create_table(db_conn)

    # Load data from CSV
    with open('user_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        data = list(reader)

    # Insert data
    insert_data(db_conn, data)
    db_conn.close()

    print("Database seeded successfully.")