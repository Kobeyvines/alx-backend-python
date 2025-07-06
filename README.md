# 📝 seed.py – Database Seeding Script Documentation

## 🎯 **Objective**
Automate the setup of the **`ALX_prodev` MySQL database** by:

1. Creating the `user_data` table with:
   - `user_id` (UUID, Primary Key, Indexed)
   - `name` (VARCHAR, NOT NULL)
   - `email` (VARCHAR, NOT NULL)
   - `age` (DECIMAL, NOT NULL)
2. Populating the table with sample data from `user_data.csv`.

---

## 🔧 **Script Overview**

### **Prototypes Implemented**

- `connect_db()`: Connects to the MySQL server.
- `create_database(connection)`: Creates the `ALX_prodev` database if it does not exist.
- `connect_to_prodev()`: Connects to the `ALX_prodev` database.
- `create_table(connection)`: Creates the `user_data` table if it does not exist.
- `insert_data(connection, data)`: Inserts user data into the table if it does not already exist (checked via email uniqueness).

---

## 📂 **Required Files**

- `seed.py` – The main Python script.
- `user_data.csv` – CSV file containing user data in the following format:

```csv
name,email,age
Alice,alice@example.com,25
Bob,bob@example.com,30
Charlie,charlie@example.com,22
