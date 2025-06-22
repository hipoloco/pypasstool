"""
passgenerator.py

Este módulo contiene funciones para interactuar con la base de datos SQLite
relacionadas con la generación de contraseñas.
"""

import sqlite3

def find_password(db_conn, hashed_password):
    """
    Busca una contraseña hasheada en la base de datos.

    Args:
        db_conn (sqlite3.Connection): Conexión a la base de datos SQLite.
        hashed_password (str): Contraseña hasheada a buscar.

    Returns:
        bool: True si la contraseña existe, False en caso contrario.
    """
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