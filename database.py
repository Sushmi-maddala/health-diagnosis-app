import sqlite3

def init_db():
    conn = sqlite3.connect("health_app.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            weight REAL,
            allergies TEXT
        )
    """)

    # Records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symptom_list TEXT,
            diagnosis TEXT,
            diet_plan TEXT
        )
    """)

    conn.commit()
    conn.close()
