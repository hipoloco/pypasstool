import time
from getpass import getpass

from modules.passutils import LOW_COMP_SYMB, MED_COMP_SYMB, HIGH_COMP_SYMB, DIGITS, LOWER, UPPER, PasswordInfo, show_password_summary
from modules.utils import clear_console, cprint,handle_task_stop,handle_program_exit, show_header

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
        passinfo = PasswordInfo()
        finishPassInfo = False
        while finishPassInfo == False:
            show_header("=== OPCIÓN 2: GENERADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")

            if passinfo.length == 0:
                largo = input("Ingresar el largo de la contraseña a generar (12-30): ") 
                if not largo.isdigit():
                    getpass("\nLo ingresado no es un número, presione ENTER para continuar")
                    continue
                
                largo = int(largo)
                    
                if largo < 12 or largo > 30:
                    getpass("\nLa contraseña debe tener entre 12 y 30 caracteres, presione ENTER para continuar")
                    continue

                passinfo.length = largo

            if passinfo.digits == None:
                has_digits = input("La contraseña tendrá números? [S/N]: ")
                if has_digits not in ["s", "S", "n", "N"]:
                    getpass("\nLa opción no es válida, presione ENTER para continuar.")
                    continue
                elif has_digits in ["n", "N"]:
                    passinfo.digits = False
                else:
                    passinfo.digits = True

            if passinfo.lower == None:
                has_lower = input("La contraseña tendrá letras minúsculas? [S/N]: ")
                if has_lower not in ["s", "S", "n", "N"]:
                    getpass("\nLa opción no es válida, presione ENTER para continuar.")
                    continue
                elif has_lower in ["n", "N"]:
                    passinfo.lower = False
                else:
                    passinfo.lower = True

            if passinfo.upper == None:
                has_upper = input("La contraseña tendrá letras mayúsculas? [S/N]: ")
                if has_upper not in ["s", "S", "n", "N"]:
                    getpass("\nLa opción no es válida, presione ENTER para continuar.")
                    continue
                elif has_upper in ["n", "N"]:
                    passinfo.upper = False
                else:
                    passinfo.upper = True

            if passinfo.highcompsymb == None and passinfo.medcompsymb == None and passinfo.lowcompsymb == None:
                has_symbols = input("La contraseña tendrá símbolos? [S/N]: ")
                if has_symbols not in ["s", "S", "n", "N"]:
                    getpass("\nLa opción no es válida, presione ENTER para continuar.")
                    continue
                elif has_symbols in ["n", "N"]:
                    passinfo.highcompsymb = False
                    passinfo.medcompsymb = False
                    passinfo.lowcompsymb = False

                    finishPassInfo = True
                else:
                    print("\nNivel de compatibilidad de símbolos:")
                    print("1) Símbolos altamente compatibles")
                    print("2) Símbolos moderadamente compatibles")
                    print("3) Símbolos menos compatibles\n")

                    symb_compatibility = input("Seleccione una opción: ")
                    if symb_compatibility not in ["1", "2", "3"]:
                        getpass("\nLa opción no es válida, presione ENTER para continuar.")
                        continue
                    elif symb_compatibility == "1":
                        passinfo.highcompsymb = True
                        passinfo.medcompsymb = False
                        passinfo.lowcompsymb = False
                    elif symb_compatibility == "2":
                        passinfo.highcompsymb = True
                        passinfo.medcompsymb = True
                        passinfo.lowcompsymb = False
                    else:
                        passinfo.highcompsymb = True
                        passinfo.medcompsymb = True
                        passinfo.lowcompsymb = True

                    finishPassInfo = True

        all_charsets = [
            DIGITS if passinfo.digits else None,
            LOWER if passinfo.lower else None,
            UPPER if passinfo.upper else None,
            HIGH_COMP_SYMB if passinfo.highcompsymb else None,
            MED_COMP_SYMB if passinfo.medcompsymb else None,
            LOW_COMP_SYMB if passinfo.lowcompsymb else None,
        ]

        selected_charsets = [charset for charset in all_charsets if charset is not None]

        if len(selected_charsets) == 0:
            selected_charsets = [DIGITS, UPPER, LOWER]
            passinfo.digits = True
            passinfo.lower = True
            passinfo.upper = True

        while True:
            contra = pass_gen(largo, selected_charsets)
            if cumple_requisitos(contra, selected_charsets):
                break

        show_header("=== OPCIÓN 2: GENERADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")

        show_password_summary(passinfo)
        print("\nLa contraseña generada es: ", end=""); cprint(contra, "G")
            
        try:
            getpass("\nPresione ENTER para volver al menú principal.")
        except KeyboardInterrupt:
            handle_program_exit()
    except KeyboardInterrupt:
        handle_task_stop()
