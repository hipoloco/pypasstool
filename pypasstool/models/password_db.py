import sqlite3

DB_NAME = 'pypasstool.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute ("""
        CREATE TABLE IF NOT EXISTS passwords(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def hash_exists(hash_hex):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM passwords WHERE hash = ?", (hash_hex,))
    result = cur.fetchone()
    conn.close()
    return result is not None


def save_hash(hash_hex):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO passwords (hash) VALUES (?)", (hash_hex,))
    conn.commit()
    conn.close()


    