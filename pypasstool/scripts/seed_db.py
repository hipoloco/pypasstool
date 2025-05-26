import os
import sqlite3

from utils.constants import DATABASE_NAME, DEVICES
from utils.utils import cprint

def seed_db(db_path=DATABASE_NAME):
    """
    Inserta los dispositivos y algoritmos de hash en la base de datos.
    """
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            seed_devices(conn)
            seed_hash_algorithms(conn)
            seed_device_hashrates(conn)
            conn.commit()
            exit_value = True
        except Exception as e:
            print(f"Error al sembrar la base de datos: {e}")
            conn.rollback()
            exit_value = False
        finally:
            if conn:
                conn.close()
            return exit_value

    else:
        print(f"La base de datos {db_path} no existe. Asegúrate de crearla primero.")
        return False

def seed_devices(db_conn):
    """
    Inserta los dispositivos encontrados en DEVICES en la tabla devices.
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
    Inserta los diferentes tipos de hashes encontrados en DEVICES en la tabla hash_algorithms.
    """
    cursor = db_conn.cursor()
    # Obtener todos los nombres de algoritmos únicos de DEVICES
    algo_names = set()
    for device in DEVICES.values():
        algo_names.update(device.get("hashrates", {}).keys())
    # Insertar cada algoritmo en la tabla hash_algorithms
    for algo in algo_names:
        cursor.execute(
            "INSERT OR IGNORE INTO hash_algorithms (algo_name, custom_algo) VALUES (?, ?)",
            (algo, False)
        )

def seed_device_hashrates(db_conn):
    """
    Inserta las tasas de hash de cada dispositivo y algoritmo en la tabla device_hashrate.
    """
    cursor = db_conn.cursor()
    # Obtener ids de dispositivos y algoritmos
    cursor.execute("SELECT id_dev, dev_name FROM devices")
    dev_map = {name: id_dev for id_dev, name in cursor.fetchall()}
    cursor.execute("SELECT id_algo, algo_name FROM hash_algorithms")
    algo_map = {name: id_algo for id_algo, name in cursor.fetchall()}

    for dev_key, device in DEVICES.items():
        dev_name = device.get("dev_name", dev_key)
        id_dev = dev_map.get(dev_name)
        for algo, hashrate in device.get("hashrates", {}).items():
            id_algo = algo_map.get(algo)
            if id_dev is not None and id_algo is not None:
                cursor.execute(
                    "INSERT OR IGNORE INTO device_hashrate (id_dev, id_algo, hashrate) VALUES (?, ?, ?)",
                    (id_dev, id_algo, hashrate)
                )

# Bloque para prevenir la ejecución directa del módulo.
if __name__ == "__main__":
    cprint("\n[*] Este módulo no puede ser ejecutado directamente.\n", "R")