import signal, sys
from getpass import getpass

import checkpass, passgenerator
from modules.constants import APP_NAME, APP_VER
from modules.utils import clear_screen, cprint, signal_handler_exit

#signal.signal(signal.SIGINT, signal_handler_exit)

def mostrar_menu():
    clear_screen()
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
            print("Ejecutar opción 3")
        elif opcion == "4":
            cprint(f"\n[*] Saliendo de {APP_NAME}.\n", "G")
            sys.exit(0)
        else:
            getpass("\nOpción incorrecta, presione ENTER para continuar.")

try:
    menu()
except KeyboardInterrupt:
    signal_handler_exit()