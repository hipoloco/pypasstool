import sqlite3
import os

from utils.constants import DATABASE_NAME, DEVICE_HASHRATES
from utils.utils import cprint

def get_db_connection(db_path=DATABASE_NAME):
    """
    Conecta a la base de datos SQLite.
    Si la base no existe, la crea y genera las tablas necesarias.
    """
    create_db = not os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    create_tables(conn)
    return conn

def create_tables(conn):
    """
    Crea las tablas necesarias en la base de datos.
    En este caso, se crea la tabla para almacenar la capacidad de cálculo de hashes del hardware.
    """
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hardware_hashrate (
            device_name TEXT NOT NULL,
            hash_algorithm TEXT NOT NULL,
            hash_rate REAL NOT NULL,
            PRIMARY KEY (device_name, hash_algorithm)
        )
    ''')
    conn.commit()
    insert_device_hashrates(conn)

def insert_device_hashrates(conn, device_hashrates=DEVICE_HASHRATES):
    """
    Inserta o actualiza en la tabla 'hardware_hashrate' los datos de hash rate para cada dispositivo.
    
    Parámetros:
    - conn: Conexión a la base de datos SQLite.
    - device_hashrates: Diccionario en el que la clave es el nombre del dispositivo y el valor es un diccionario con
      los algoritmos de hash y sus velocidades, por ejemplo:
      
      {
          "RTX 4090": {
              "BCRYPT": 1.84e5,
              "MD5": 1.641e11,
              "SHA-1": 5.06387e10
          }
      }
    """
    cursor = conn.cursor()
    for device_name, hash_dict in device_hashrates.items():
        for algorithm, rate in hash_dict.items():
            cursor.execute("""
                INSERT OR REPLACE INTO hardware_hashrate (device_name, hash_algorithm, hash_rate)
                VALUES (?, ?, ?)
            """, (device_name, algorithm, rate))
    conn.commit()

# Bloque para prevenir la ejecución directa del módulo.
if __name__ == "__main__":
    cprint("\n[*] Este módulo no puede ser ejecutado directamente.\n", "R")