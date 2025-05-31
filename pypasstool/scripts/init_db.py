import sqlite3
import os, sys

from utils.constants import DATABASE_NAME
from utils.utils import cprint

def create_db(db_path=DATABASE_NAME):
    try:
        db_conn = sqlite3.connect(db_path)
        create_tables(db_conn)
    except sqlite3.Error as e:
        if db_conn:
            db_conn.close()
        if os.path.exists(db_path):
            cprint(f"\n[!] Error inesperado al crear la base de datos.\n", "R")
            os.remove(db_path)
        else:
            cprint("\n[!] No se pudo crear el archivo de base de datos (permiso denegado o ruta inválida).\n", "R")
        sys.exit(1)

    return db_conn

def create_tables(db_conn):
    cursor = db_conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id_dev INTEGER NOT NULL,
            dev_name TEXT NOT NULL,
            PRIMARY KEY(id_dev AUTOINCREMENT) CONSTRAINT pk_dev,
            UNIQUE(dev_name) CONSTRAINT uk_dev_devname
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hash_algorithms (
            id_algo INTEGER NOT NULL,
            algo_name TEXT NOT NULL,
            custom_algo BOOLEAN NOT NULL,
            PRIMARY KEY(id_algo AUTOINCREMENT) CONSTRAINT pk_hashalgo,
            UNIQUE(algo_name) CONSTRAINT uk_hashalgo_name
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_hashrate (
            id_dev INTEGER NOT NULL,
            id_algo INTEGER NOT NULL,
            hashrate REAL NOT NULL,
            PRIMARY KEY(id_dev, id_algo) CONSTRAINT pk_devhash,
            FOREIGN KEY(id_dev) REFERENCES devices(id_dev) CONSTRAINT fk_devhash_iddev,
            FOREIGN KEY(id_algo) REFERENCES hash_algorithms(id_algo) CONSTRAINT fk_devhash_idalgo
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id_pwd INTEGER NOT NULL,
            hashedpwd TEXT NOT NULL,
            PRIMARY KEY(id_pwd AUTOINCREMENT) CONSTRAINT pk_pwd,
            UNIQUE(hashedpwd) CONSTRAINT uk_pwd_hashedpwd
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hashes (
            id_pwd INTEGER NOT NULL,
            id_algo INTEGER NOT NULL,
            hash TEXT NOT NULL,
            PRIMARY KEY(id_pwd, id_algo) CONSTRAINT pk_hash,
            FOREIGN KEY(id_pwd) REFERENCES passwords(id_pwd) CONSTRAINT fk_hash_idpwd,
            FOREIGN KEY(id_algo) REFERENCES hash_algorithms(id_algo) CONSTRAINT fk_hash_idalgo
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_props (
            id_pwdprop INTEGER NOT NULL,
            pwd_length INTEGER NOT NULL,
            has_digits BOOLEAN NOT NULL,
            has_lower BOOLEAN NOT NULL,
            has_upper BOOLEAN NOT NULL,
            has_highsymb BOOLEAN NOT NULL,
            has_midsymb BOOLEAN NOT NULL,
            has_lowsymb BOOLEAN NOT NULL,
            PRIMARY KEY(id_pwdprop AUTOINCREMENT) CONSTRAINT pk_pwdprops,
            UNIQUE(
                pwd_length, has_digits, has_lower, has_upper, 
                has_highsymb, has_midsymb, has_lowsymb
            ) CONSTRAINT uk_pwdprops_allprops
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_bruteforce (
            id_pwdprop INTEGER NOT NULL,
            id_dev INTEGER NOT NULL,
            id_algo INTEGER NOT NULL,
            num_devices INTEGER NOT NULL,
            bruteforce_time REAL NOT NULL,
            PRIMARY KEY(id_pwdprop, id_dev, id_algo, num_devices) CONSTRAINT pk_pwdbrute,
            FOREIGN KEY(id_pwdprop) REFERENCES password_props(id_pwdprop) CONSTRAINT fk_pwdbrute_idpwdprop,
            FOREIGN KEY(id_dev, id_algo) REFERENCES device_hashrate(id_dev, id_algo) CONSTRAINT fk_pwdbrute_devhashid
        )
    ''')

    db_conn.commit()

# Bloque para prevenir la ejecución directa del módulo.
if __name__ == "__main__":
    cprint("\n[*] Este módulo no puede ser ejecutado directamente.\n", "R")