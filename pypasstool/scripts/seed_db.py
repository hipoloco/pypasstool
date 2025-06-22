"""
seed_db.py

Este módulo se encarga de poblar la base de datos con los dispositivos y algoritmos de hash definidos en `DEVICES` y `CUSTOM_HASH_ALGORITHMS`.
"""

import sys

from utils.constants import DEVICES, CUSTOM_HASH_ALGORITHMS
from utils.utils import cprint

def seed_db(db_conn):
    """
    Inserta los dispositivos y algoritmos de hash en la base de datos.

    Args:
        db_conn (sqlite3.Connection): Objeto de conexión a la base de datos.

    Raises:
        Exception: Si ocurre un error al insertar los datos en la base de datos.
    """
    try:
        seed_devices(db_conn)
        seed_hash_algorithms(db_conn)
        seed_device_hashrates(db_conn)
        db_conn.commit()
        exit_value = True
    except Exception as e:
        cprint(f"\n[!] Error inesperado al poblar la base de datos.\n", "R")
        db_conn.rollback()
        exit_value = False
    finally:
        if not exit_value:
            db_conn.close()
            sys.exit(1)

def seed_devices(db_conn):
    """
    Inserta los dispositivos definidos en DEVICES en la tabla devices.
    Si un dispositivo ya existe, se ignora la inserción.

    Args:
        db_conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    """
    cursor = db_conn.cursor()
    for dev_key, device in DEVICES.items():
        dev_name = device.get("dev_name", dev_key)
        cursor.execute(
            "INSERT OR IGNORE INTO devices (dev_name) VALUES (?)",
            (dev_name,)
        )

def seed_hash_algorithms(db_conn):
    """
    Inserta los algoritmos de hash únicos en la tabla hash_algorithms.
    Si un algoritmo ya existe, se ignora la inserción.

    Args:
        db_conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    """
    cursor = db_conn.cursor()
    # Obtener todos los nombres de algoritmos únicos de DEVICES
    algo_names = set()
    for device in DEVICES.values():
        algo_names.update(device.get("hashrates", {}).keys())
    # Agregar algoritmos personalizados
    algo_names.update(CUSTOM_HASH_ALGORITHMS)
    # Insertar cada algoritmo en la tabla hash_algorithms
    for algo in algo_names:
        cursor.execute(
            "INSERT OR IGNORE INTO hash_algorithms (algo_name) VALUES (?)",
            (algo,)
        )

def seed_device_hashrates(db_conn):
    """
    Inserta las tasas de hash de cada dispositivo y algoritmo en la tabla device_hashrate.
    Si una combinación de dispositivo y algoritmo ya existe, se ignora la inserción.

    Args:
        db_conn (sqlite3.Connection): Objeto de conexión a la base de datos.
    """
    cursor = db_conn.cursor()
    # Obtener ids de dispositivos y sus nombres
    cursor.execute("SELECT id_dev, dev_name FROM devices")
    # Crear un diccionario para mapear nombres de dispositivos a sus ids
    dev_map = {name: id_dev for id_dev, name in cursor.fetchall()}
    # Obtener ids de algoritmos y sus nombres
    cursor.execute("SELECT id_algo, algo_name FROM hash_algorithms")
    # Crear un diccionario para mapear nombres de algoritmos a sus ids
    algo_map = {name: id_algo for id_algo, name in cursor.fetchall()}

    # Recorrer todos los dispositivos definidos en DEVICES
    for dev_key, device in DEVICES.items():
        dev_name = device.get("dev_name", dev_key)
        id_dev = dev_map.get(dev_name)
        # Recorrer todos los algoritmos y sus tasas de hash para el dispositivo actual
        for algo, hashrate in device.get("hashrates", {}).items():
            id_algo = algo_map.get(algo)
            # Si existen tanto el dispositivo como el algoritmo en la base de datos
            if id_dev is not None and id_algo is not None:
                # Insertar la relación dispositivo-algoritmo y su hashrate en la tabla device_hashrate
                cursor.execute(
                    "INSERT OR IGNORE INTO device_hashrate (id_dev, id_algo, hashrate) VALUES (?, ?, ?)",
                    (id_dev, id_algo, hashrate)
                )

# Bloque para prevenir la ejecución directa del módulo.
if __name__ == "__main__":
    cprint("\n[*] Este módulo no puede ser ejecutado directamente.\n", "R")