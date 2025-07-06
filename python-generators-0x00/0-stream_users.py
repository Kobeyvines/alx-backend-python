#!/usr/bin/env python3
import mysql.connector

def stream_users():
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="alx_user",
        password="strong_password",
        database="ALX_prodev"
    )
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    
    #loop through the cursor directly yields one row at a time
    for row in cursor:
        yield row
        
    #close connection
    cursor.close()
    connection.close()
