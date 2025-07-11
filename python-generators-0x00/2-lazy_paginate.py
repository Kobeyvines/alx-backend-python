#!/usr/bin/env python3
import mysql.connector


# 🔧 Connect to the ALX_prodev database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="strong_password",
        database="ALX_prodev",
    )


# Function to fetch a single page with given offset
def paginate_users(page_size, offset):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


# Generator to lazily paginate
def lazy_paginate(page_size):
    offset = 0
    while True:  # single loop allowed
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # yields each page when needed
        offset += page_size
