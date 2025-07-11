#!/usr/bin/env python3

import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=()):
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.conn.close()

#### Use the context manager to fetch users older than 25

with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print(results)
