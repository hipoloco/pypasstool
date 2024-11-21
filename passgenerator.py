from modules.passutils import QWERTY_SYMB, COMM_SYMB, SEC_SYMB, NUMS, LOWER, UPPER
from getpass import getpass
from modules.utils import clear_screen, cprint
import time

def pass_gen(largo):
    contra = ""
    allchars = list(QWERTY_SYMB) + list(COMM_SYMB) + list(SEC_SYMB) + list(NUMS) + list(LOWER) + list(UPPER)

    if largo <= 0:
        print("El largo de la contraseña debe ser mayor a 0")
    
    seed = int(time.time() * 1000)  # Usa el tiempo actual como semilla para que las contraseñas generadas sean siempre distintas
    for i in range(largo):
        seed = (seed * 9301 + 49297) % 233280
        index = seed % len(allchars)
        contra += allchars[index]

    return contra

def passgenerator():
    while True:
        try:
            clear_screen()
            cprint("=== OPCIÓN 2: GENERADOR DE CONTRASEÑAS ===\n", "Y")
            
            while True:
                largo = input("Ingresar el largo de la contraseña a generar (8-18): ")
                
                # Verificar si el input es un número
                if not largo.isdigit():
                    getpass("\nLo ingresado no es un número, presione ENTER para continuar")
                    continue
                
                largo = int(largo)

                # Verifica que el número esté dentro del rango permitido
                if largo < 8 or largo > 18:
                    getpass("\nLa contraseña debe tener entre 8 y 18 caracteres, presione ENTER para continuar")
                    continue

                # Si el número es válido, genera la contraseña
                contra = pass_gen(largo)
                print("\nSu contraseña es:", contra)
                
                # Esperar que el usuario presione ENTER antes de limpiar la pantalla
                getpass("\nPresione ENTER para continuar")
                break  # Salir del ciclo
            
        except ValueError as e:
            getpass("\nOcurrió un error, presione ENTER para continuar")
