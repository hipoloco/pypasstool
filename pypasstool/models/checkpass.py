"""
checkpass.py

Este módulo contiene funciones para interactuar con la base de datos SQLite
relacionadas con el análisis de contraseñas.
"""
import sqlite3

def get_devices(db_conn):
    """
    Obtiene la lista de dispositivos desde la base de datos.

    Args:
        db_conn (sqlite3.Connection): Conexión a la base de datos SQLite.

    Returns:
        list: Lista de dispositivos con sus nombres e ID's.
    """
    cursor = db_conn.cursor()
    cursor.execute("SELECT id_dev, dev_name FROM devices ORDER BY dev_name")
    return cursor.fetchall()

def get_device_hashes(db_conn, id_dev):
    """
    Obtiene los algoritmos de hash y sus hashrates para un dispositivo específico.
    
    Args:
        db_conn (sqlite3.Connection): Conexión a la base de datos SQLite.
        id_dev (int): ID del dispositivo para el cual se desean obtener los algoritmos de hash.
        
    Returns:
        list: Lista de tuplas con el ID del algoritmo, nombre del algoritmo y su hashrate.
    """

    cursor = db_conn.cursor()
    cursor.execute("""
        SELECT ha.id_algo, ha.algo_name, dhr.hashrate
        FROM hash_algorithms ha
        JOIN device_hashrate dhr ON ha.id_algo = dhr.id_algo
        WHERE dhr.id_dev = ?
        ORDER BY ha.algo_name
    """, (id_dev,))

    return cursor.fetchall()

def find_password_props_id(db_conn, passinfo):
    """
    Busca en la tabla password_props un registro que coincida con las propiedades de passinfo.

    Args:
        db_conn: Conexión a la base de datos.
        passinfo: Objeto PasswordInfo con las propiedades de la contraseña.

    Returns:
        tuple: Tupla con el ID de las propiedades de la contraseña si se encuentra, None en caso contrario.
    """
    cursor = db_conn.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("""
        SELECT id_pwdprop FROM password_props
        WHERE pwd_length = ?
          AND has_digits = ?
          AND has_lower = ?
          AND has_upper = ?
          AND has_highsymb = ?
          AND has_midsymb = ?
          AND has_lowsymb = ?
        LIMIT 1
    """, (
        passinfo.length,
        int(passinfo.digits),
        int(passinfo.lower),
        int(passinfo.upper),
        int(passinfo.highcompsymb),
        int(passinfo.medcompsymb),
        int(passinfo.lowcompsymb)
    ))

    row = cursor.fetchone()
    return row[0] if row else None

def insert_password_props(db_conn, passinfo):
    """
    Inserta un nuevo registro en la tabla password_props con las propiedades de la contraseña.

    Args:
        db_conn: Conexión a la base de datos.
        passinfo: Objeto PasswordInfo con las propiedades de la contraseña.

    Returns:
        int: El id_pwdprop recién insertado.
    """
    cursor = db_conn.cursor()
    cursor.execute("""
        INSERT INTO password_props (
            pwd_length, has_digits, has_lower, has_upper,
            has_highsymb, has_midsymb, has_lowsymb
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        passinfo.length,
        int(passinfo.digits),
        int(passinfo.lower),
        int(passinfo.upper),
        int(passinfo.highcompsymb),
        int(passinfo.medcompsymb),
        int(passinfo.lowcompsymb)
    ))
    db_conn.commit()
    return cursor.lastrowid

def find_bruteforce_entry(db_conn, id_pwdprop, id_dev, id_algo):
    """
    Busca una coincidencia exacta en la tabla password_bruteforce para los parámetros dados.

    Args:
        db_conn: Conexión a la base de datos.
        id_pwdprop (int): ID de las propiedades de la contraseña.
        id_dev (int): ID del dispositivo.
        id_algo (int): ID del algoritmo de hash.

    Returns:
        dict | None: Diccionario con los datos encontrados o None si no existe coincidencia.
    """
    cursor = db_conn.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("""
        SELECT id_pwdprop, id_dev, id_algo, bruteforce_time
        FROM password_bruteforce
        WHERE id_pwdprop = ? AND id_dev = ? AND id_algo = ?
        LIMIT 1
    """, (id_pwdprop, id_dev, id_algo))

    return cursor.fetchone()

def insert_password_bruteforce(db_conn, id_pwdprop, id_dev, id_algo, bruteforce_time):
    """
    Inserta en la tabla password_bruteforce una combinación específica de id_pwdprop,
    id_dev, id_algo y bruteforce_time.

    Args:
        db_conn: Conexión a la base de datos.
        id_pwdprop (int): ID de las propiedades de la contraseña.
        id_dev (int): ID del dispositivo.
        id_algo (int): ID del algoritmo de hash.
        bruteforce_time (float): Tiempo de ruptura calculado.
    """
    cursor = db_conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO password_bruteforce (id_pwdprop, id_dev, id_algo, bruteforce_time)
        VALUES (?, ?, ?, ?)
    """, (id_pwdprop, id_dev, id_algo, bruteforce_time))
    db_conn.commit()

def update_bruteforce_time(db_conn, id_pwdprop, id_dev, id_algo, bruteforce_time):
    """
    Actualiza el campo bruteforce_time para una combinación específica en password_bruteforce.

    Args:
        db_conn: Conexión a la base de datos.
        id_pwdprop (int): ID de las propiedades de la contraseña.
        id_dev (int): ID del dispositivo.
        id_algo (int): ID del algoritmo de hash.
        bruteforce_time (float): Tiempo de ruptura calculado.
    """
    cursor = db_conn.cursor()
    cursor.execute("""
        UPDATE password_bruteforce
        SET bruteforce_time = ?
        WHERE id_pwdprop = ? AND id_dev = ? AND id_algo = ?
    """, (bruteforce_time, id_pwdprop, id_dev, id_algo))
    db_conn.commit()