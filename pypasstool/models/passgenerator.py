import sqlite3

def find_password(db_conn, hashed_password):
    
    cursor = db_conn.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("""
        SELECT hashedpwd FROM passwords
        WHERE hashedpwd = ?
        LIMIT 1
    """, (
        hashed_password,
    ))

    row = cursor.fetchone()
    return True if row else False

def insert_password(db_conn, hassed_password):
    cursor = db_conn.cursor()
    cursor.execute("""
        INSERT INTO passwords (hashedpwd)
        VALUES (?)
    """, (hassed_password,))
    db_conn.commit()