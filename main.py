import signal, sys
from getpass import getpass

import checkpass, passgenerator, hashpass
from modules.constants import APP_NAME, APP_VER
from modules.utils import clear_console, cprint, handle_program_exit

#signal.signal(signal.SIGINT, signal_handler_exit)

def mostrar_menu():
    clear_console()
    cprint(f"=== {APP_NAME} v{APP_VER} - MENÚ PRINCIPAL ===\n", "Y")
    print("1. Analizar contraseña")
    print("2. Generar contraseña")
    print("3. Hashear contraseña")
    print("4. Salir\n")
    
    opcion = input("Seleccione una opción: ")
    return opcion

def menu():
    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            checkpass.checkpass()
        elif opcion == "2":
            passgenerator.passgenerator()
        elif opcion == "3":
            hashpass.hashpass()
        elif opcion == "4":
            cprint(f"\n[*] Saliendo de {APP_NAME}.\n", "G1")
            sys.exit(0)
        else:
            getpass("\nOpción incorrecta, presione ENTER para continuar.")

try:
    menu()
except KeyboardInterrupt:
    handle_program_exit()