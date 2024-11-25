import signal
from getpass import getpass

import checkpass, passgenerator
from modules.utils import clear_screen, cprint, signal_handler

signal.signal(signal.SIGINT, signal_handler)

def mostrar_menu():
    clear_screen()
    cprint("===== MENÚ PRINCIPAL =====\n", "Y")
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
            print("Ejecutar opción 4")
        else:
            getpass("\nOpción incorrecta, presione ENTER para continuar.")

menu()