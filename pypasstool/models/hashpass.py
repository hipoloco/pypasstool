"""
hashpass.py

Este módulo contiene funciones para interactuar con la base de datos SQLite
relacionadas con el hasheo de contraseñas.
"""
import sqlite3

def get_hash_algo(db_conn):
    """
    Obtiene la lista de algoritmos de hash desde la base de datos.

    Args:
        db_conn (sqlite3.Connection): Conexión a la base de datos SQLite.

    Returns:
        list: Lista de tuplas con el ID del algoritmo y su nombre.
    """
    cursor = db_conn.cursor()
    cursor.execute("SELECT id_algo, algo_name FROM hash_algorithms ORDER BY algo_name")
    return cursor.fetchall()

def find_password_id(db_conn, hashed_password):
    """
    Busca el ID de una contraseña hasheada en la base de datos.

    Args:
        db_conn (sqlite3.Connection): Conexión a la base de datos SQLite.
        hashed_password (str): Contraseña hasheada a buscar.

    Returns:
        int | None: ID de la contraseña si se encuentra, None en caso contrario.
    """
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

def find_password_hash(db_conn, id_pwd, id_algo):
    """
    Busca el hash de una para una contraseña y un algoritmo dado en la base de datos.

    Args:
        db_conn (sqlite3.Connection): Conexión a la base de datos SQLite.
        id_pwd (int): ID de la contraseña.
        id_algo (int): ID del algoritmo de hash.

    Returns:
        str | None: El hash de la contraseña si se encuentra, None en caso contrario.
    """
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
    """
    Inserta un nuevo hash de contraseña en la base de datos.

    Args:
        db_conn (sqlite3.Connection): Conexión a la base de datos SQLite.
        id_pwd (int): ID de la contraseña.
        id_algo (int): ID del algoritmo de hash.
        hash (str): El hash de la contraseña.
    """
    cursor = db_conn.cursor()
    cursor.execute("""
        INSERT INTO hashes (id_pwd, id_algo, hash)
        VALUES (?, ?, ?)
    """, (id_pwd, id_algo, hash))
    db_conn.commit()