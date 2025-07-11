#!/usr/bin/env python3

import sqlite3
import functools
from datetime import datetime  # Required import

# Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query')
        if query is None and len(args) > 0:
            query = args[0]
        print(f"[{datetime.now()}] Executing SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query with timestamp
users = fetch_all_users(query="SELECT * FROM users")
print(users)
