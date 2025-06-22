"""
common.py

Este módulo contiene funciones comunes para interactuar con la base de datos SQLite.
"""

def insert_password(db_conn, hashedpwd):
    """
    Inserta una contraseña hasheada en la base de datos.

    Args:
        db_conn (sqlite3.Connection): Conexión a la base de datos SQLite.
        hashedpwd (str): Contraseña hasheada a insertar.

    Returns:
        int: ID de la contraseña insertada.
    """
    cursor = db_conn.cursor()
    cursor.execute("""
        INSERT INTO passwords (hashedpwd)
        VALUES (?)
    """, (hashedpwd,))
    db_conn.commit()
    return cursor.lastrowid