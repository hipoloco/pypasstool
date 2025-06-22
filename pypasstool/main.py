"""
main.py

Punto de entrada principal para la aplicación PyPassTool.
Este script inicializa la aplicación, crea y siembra la base de datos,
y muestra el menú principal para interactuar con las diferentes funcionalidades de la herramienta.
"""
import sys
from getpass import getpass

import checkpass, passgenerator, hashpass
from utils.constants import APP_NAME, APP_VER
from utils.utils import clear_console, cprint, handle_program_exit

from scripts.init_db import create_db
from scripts.seed_db import seed_db

def init_app():
    """
    Inicializa la base de datos y siembra los datos iniciales.

    Returns:
        sqlite3.Connection: Conexión a la base de datos SQLite creada o existente.
    """
    db_conn = create_db()
    seed_db(db_conn)
    return db_conn

def mostrar_menu():
    """
    Muestra el menú principal de la aplicación y solicita al usuario seleccionar una opción.

    Returns:
        str: Opción ingresada por el usuario.
    """
    clear_console()
    cprint(f"=== {APP_NAME} v{APP_VER} - MENÚ PRINCIPAL ===\n", "Y")
    print("1. Analizar contraseña")
    print("2. Generar contraseña")
    print("3. Hashear contraseña")
    print("4. Salir\n")
    
    opcion = input("Seleccione una opción: ")
    return opcion

def menu(db_conn):
    """
    Muestra el menú principal y maneja las opciones seleccionadas por el usuario.

    Args:
        db_conn: Conexión a la base de datos SQLite.
    """
    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            checkpass.checkpass(db_conn)
        elif opcion == "2":
            passgenerator.passgenerator(db_conn)
        elif opcion == "3":
            hashpass.hashpass(db_conn)
        elif opcion == "4":
            cprint(f"\n[*] Saliendo de {APP_NAME}.\n", "G")
            db_conn.close()
            sys.exit(0)
        else:
            getpass("\nOpción incorrecta, presione ENTER para continuar.")

if __name__ == "__main__":
    try:
        db_conn = init_app()
        menu(db_conn)
    except KeyboardInterrupt:
        handle_program_exit()