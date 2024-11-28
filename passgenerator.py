from modules.passutils import LOW_COMP_SYMB, MED_COMP_SYMB, HIGH_COMP_SYMB, DIGITS, LOWER, UPPER,PasswordInfo,password_has_chartype
from getpass import getpass
from modules.utils import clear_console, cprint,handle_task_stop,handle_program_exit
from checkpass import show_password_summary,analyze_password_props,set_password_secururity
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
        "1": ("Símbolos de baja compatibilidad", LOW_COMP_SYMB),
        "2": ("Símbolos de compatibilidad media", MED_COMP_SYMB),
        "3": ("Símbolos de alta compatibilidad", HIGH_COMP_SYMB),
        "4": ("Números", DIGITS),
        "5": ("Letras minúsculas", LOWER),
        "6": ("Letras mayúsculas", UPPER),
    }
    
    charsets = []
    print("Seleccione los conjuntos de caracteres a incluir en la contraseña:\n")

    for _, (desc, charset) in opciones.items():
        while True:
            respuesta = input (f"¿Desea incluir {desc}? (Y/N): ").strip().upper()
            print("")
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
        clear_console()
        cprint("=== OPCIÓN 2: GENERADOR DE contraSEÑAS ===\n", "Y")
        
        while True:
            largo = input("Ingresar el largo de la contraseña a generar (12-30): ")
            
            if not largo.isdigit():
                getpass("\nLo ingresado no es un número, presione ENTER para continuar")
                clear_console()
                continue
            
            largo = int(largo)
            
            if largo < 12 or largo > 30:
                getpass("\nLa contraseña debe tener entre 12 y 30 caracteres, presione ENTER para continuar")
                clear_console()
                continue

            # Permitir al usuario seleccionar los conjuntos de caracteres
            charsets = seleccionar_conjuntos()

            while True:
                contra = pass_gen(largo, charsets)
                if cumple_requisitos(contra, charsets):
                    break

            print("\nSu contraseña es:", end=" "); cprint(contra, "G")
            analize=input("Desea analizar la contraseña generada? (Y para analizar, otra opcion para salir)").strip().upper()
            if analize == "Y":
                passinfo=PasswordInfo
                analyze_password_props(contra,passinfo)
                show_password_summary(passinfo)
            try:
                getpass("\nPresione ENTER para volver al menú principal.")
            except KeyboardInterrupt:
                handle_program_exit()
    except:
        handle_task_stop
