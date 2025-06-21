import sqlite3

def get_hash_algo(db_conn):
   
    cursor = db_conn.cursor()
    cursor.execute("SELECT id_algo, algo_name FROM hash_algorithms ORDER BY algo_name")
    return cursor.fetchall()

def find_password_id(db_conn, hashed_password):
    
    cursor = db_conn.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("""
        SELECT id_pwd FROM passwords
        WHERE hashedpwd = ?
        LIMIT 1
    """, (
        hashed_password,
    ))

    row = cursor.fetchone()
    return row[0] if row else None

def find_password_hash(db_conn, id_pwd,id_algo):
    cursor = db_conn.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("""
        SELECT hash FROM hashes
        WHERE id_pwd  = ? AND id_algo = ?
        LIMIT 1
    """, (
        id_pwd, id_algo
    ))

    row = cursor.fetchone()
    return row[0] if row else None

def insert_password_hash(db_conn, id_pwd, id_algo, hash):
    cursor = db_conn.cursor()
    cursor.execute("""
        INSERT INTO hashes (id_pwd, id_algo, hash)
        VALUES (?, ?, ?)
    """, (id_pwd, id_algo, hash))
    db_conn.commit()


def insert_password(db_conn, hashedpwd):
    cursor = db_conn.cursor()
    cursor.execute("""
        INSERT INTO passwords (hashedpwd)
        VALUES (?)
    """, (hashedpwd,))
    db_conn.commit()
    return cursor.lastrowid




    