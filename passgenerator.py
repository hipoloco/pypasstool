from modules.passutils import QWERTY_SYMB, COMM_SYMB, SEC_SYMB, NUMS, LOWER, UPPER
from getpass import getpass
from modules.utils import clear_screen, cprint
import time

def pass_gen(largo, charsets): #la funcion genera una contraseña con el largo que indica el usuario y los sets de caracteres elegidos
    
    contra = ""
    allchars = []
    for charset in charsets:
        allchars += list(charset)

    if largo <= 0:
        print("El largo de la contraseña debe ser mayor a 0")
        return ""
    
    seed = int(time.time() * 1000)  # Usa el tiempo actual como semilla
    for i in range(largo):
        seed = (seed * 9301 + 49297) % 233280
        index = seed % len(allchars)
        contra += allchars[index]

    return contra

def cumple_requisitos(contra, charsets): #esta funcion verifica que la contraseña generada cumpla con los requisitos de caracteres indicados por el usuario
    
    return all(any(c in charset for c in contra) for charset in charsets)
 
def seleccionar_conjuntos(): #Permite al usuario seleccionar los caracteres que desea incluir en la contraseña generada.
    
    opciones = {
        "1": ("Símbolos especiales (QWERTY)\n ¡ATENCIÓN!, puede que estos simbolos no sean aceptados por algunos sitios para su contraseña", QWERTY_SYMB),
        "2": ("Símbolos de comunicación", COMM_SYMB),
        "3": ("Símbolos comunes", SEC_SYMB),
        "4": ("Números", NUMS),
        "5": ("Letras minúsculas", LOWER),
        "6": ("Letras mayúsculas", UPPER),
    }
    
    charsets = []
    print("Seleccione los conjuntos de caracteres a incluir en la contraseña:\n")

    for _, (desc, charset) in opciones.items():
        while True:
            respuesta = input(f"¿Desea incluir {desc}? (Y/N):\n ").strip().upper()
            if respuesta in ("Y", "N"):
                if respuesta == "Y":
                    charsets.append(charset)
                break
            else:
                print("Respuesta inválida. Por favor, ingrese 'Y' para sí o 'N' para no.")
    
    if not charsets:
        print("No seleccionó ningún conjunto. Se usarán todos por defecto.")
        charsets = [v[1] for v in opciones.values()]
    
    return charsets

def passgenerator():
    try:
        clear_screen()
        cprint("=== OPCIÓN 2: GENERADOR DE CONTRASEÑAS ===\n", "Y")
        
        while True:
            largo = input("Ingresar el largo de la contraseña a generar (8-18): ")
            
            if not largo.isdigit():
                getpass("\nLo ingresado no es un número, presione ENTER para continuar")
                clear_screen()
                continue
            
            largo = int(largo)
            
            if largo < 8 or largo > 18:
                getpass("\nLa contraseña debe tener entre 8 y 18 caracteres, presione ENTER para continuar")
                clear_screen()
                continue

            # Permitir al usuario seleccionar los conjuntos de caracteres
            charsets = seleccionar_conjuntos()

            while True:
                contra = pass_gen(largo, charsets)
                if cumple_requisitos(contra, charsets):
                    break

            print("\nSu contraseña es:", contra)
            getpass("\nPresione ENTER para volver al menú principal")
            break  # Salir del ciclo principal
        
    except ValueError as e:
        getpass("\nOcurrió un error, presione ENTER para continuar")

