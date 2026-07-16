import sqlite3

DB_NAME = "database/database.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    return conn


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_user(name, email, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users(name,email,phone) VALUES(?,?,?)",
        (name, email, phone)
    )

    conn.commit()
    conn.close()


def get_all_users():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT name,email,phone FROM users")

    rows = cur.fetchall()

    conn.close()

    return rows