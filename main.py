"""
main.py

Este módulo sirve como punto de entrada para la aplicación. Proporciona un menú principal 
que permite al usuario seleccionar entre diferentes funcionalidades: analizar contraseñas, 
generar contraseñas, o hashear contraseñas. También maneja la interacción del usuario y 
la navegación entre las opciones de manera controlada y segura.
"""

import sys
from getpass import getpass

import checkpass, passgenerator, hashpass
from modules.constants import APP_NAME, APP_VER
from modules.utils import cprint, handle_program_exit, show_header

def mostrar_menu():
    """
    Muestra el menú principal de la aplicación y solicita al usuario seleccionar una opción.

    Returns:
        str: Opción seleccionada por el usuario.
    """

    show_header(f"=== {APP_NAME} v{APP_VER} - MENÚ PRINCIPAL ===\n")
    print("1. Analizar contraseña")
    print("2. Generar contraseña")
    print("3. Hashear contraseña")
    print("4. Salir\n")
    
    opcion = input("Seleccione una opción: ")
    return opcion

def menu():
    """
    Controla la navegación en el menú principal de la aplicación.

    Permite al usuario seleccionar una de las funcionalidades disponibles:
    - Analizar contraseña (opción 1)
    - Generar contraseña (opción 2)
    - Hashear contraseña (opción 3)
    - Salir del programa (opción 4)

    Maneja entradas inválidas y permite reintentar la selección. También
    maneja la interrupción por teclado (Ctrl+C) para una salida controlada.
    """
    
    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            checkpass.checkpass()  # Llama al módulo de análisis de contraseñas
        elif opcion == "2":
            passgenerator.passgenerator()  # Llama al módulo de generación de contraseñas
        elif opcion == "3":
            hashpass.hashpass()  # Llama al módulo de hashing de contraseñas
        elif opcion == "4":
            cprint(f"\n[*] Saliendo de {APP_NAME}.\n", "B")
            sys.exit(0)  # Finaliza el programa
        else:
            getpass("\nOpción incorrecta, presione ENTER para continuar.")  # Maneja opciones inválidas

# Bloque principal para iniciar el programa y manejar interrupciones controladas
try:
    menu()
except KeyboardInterrupt:
    handle_program_exit()