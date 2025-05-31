import signal, sys, os, sqlite3
from getpass import getpass

import checkpass, passgenerator, hashpass
from utils.constants import APP_NAME, APP_VER
from utils.utils import clear_console, cprint, handle_program_exit

from scripts.init_db import create_db
from scripts.seed_db import seed_db

#signal.signal(signal.SIGINT, signal_handler_exit)

def init_app():
    db_conn = create_db()
    seed_db(db_conn)
    return db_conn

def mostrar_menu():
    clear_console()
    cprint(f"=== {APP_NAME} v{APP_VER} - MENÚ PRINCIPAL ===\n", "Y")
    print("1. Analizar contraseña")
    print("2. Generar contraseña")
    print("3. Hashear contraseña")
    print("4. Salir\n")
    
    opcion = input("Seleccione una opción: ")
    return opcion

def menu(db_conn):
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

try:
    db_conn = init_app()
    menu(db_conn)
except KeyboardInterrupt:
    handle_program_exit()