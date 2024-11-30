#import random
import time
from getpass import getpass

from modules.passutils import LOW_COMP_SYMB, MED_COMP_SYMB, HIGH_COMP_SYMB, DIGITS, LOWER, UPPER, PasswordInfo, show_password_summary
from modules.utils import clear_console, cprint,handle_task_stop,handle_program_exit, show_header

def password_generator(length, charset_list): #la funcion genera una contraseña con el largo que indica el usuario y los sets de caracteres elegidos

    if length <= 0:
        print("El largo de la contraseña debe ser mayor a 0")
        return ""

    #allchars = []
    #for charset in charsets:
    #    allchars += list(charset)
    allchars = ''.join(''.join(charset) for charset in charset_list)

    password = ""
    seed = int(time.time() * 1000)  # Usa el tiempo actual como semilla
    for i in range(length):
        seed = (seed * 9301 + 49297) % 233280
        index = seed % len(allchars)
        password += allchars[index]
    
    #return password
    #return ''.join(random.choices(allchars, k=length))

    if all(any(char in charset for char in password) for charset in charset_list):
        return password
    else:
        return password_generator(length, charset_list)

#def cumple_requisitos(password, charset_list): #esta funcion verifica que la contraseña generada cumpla con los requisitos de caracteres indicados por el usuario
#    
#    return all(any(char in charset for char in password) for charset in charset_list)

def set_password_length():
    password_length = input("Ingresar el largo de la contraseña a generar (12-30): ") 
    if not password_length.isdigit():
        getpass("\nLo ingresado no es un número, presione ENTER para continuar")
        return None
    
    password_length = int(password_length)
    if password_length < 12 or password_length > 30:
        getpass("\nLa contraseña debe tener entre 12 y 30 caracteres, presione ENTER para continuar")
        return None
    
    return password_length

def ask_yes_no(question):
    answer = input(f"{question} [S/N]: ")
    if answer.lower() not in ['s', 'n']:
        input("\nLa opción no es válida, presione ENTER para continuar.")
        return None
    return answer.lower() == 's'

def passgenerator():
    try:
        passinfo = PasswordInfo()
        finishPassInfo = False
        while finishPassInfo == False:
            show_header("=== OPCIÓN 2: GENERADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")

            if passinfo.length == None:
                passinfo.length = set_password_length()
                if passinfo.length == None:
                    continue

            options = [
                ('digits', 'La contraseña tendrá números?'),
                ('lower', 'La contraseña tendrá letras minúsculas?'),
                ('upper', 'La contraseña tendrá letras mayúsculas?')
            ]

            invalid_option = False

            for attr, question in options:
                if getattr(passinfo, attr) == None:
                    result = ask_yes_no(question)
                    if result == None:
                        invalid_option = True
                        break  # Sale del bucle for y vuelve al inicio del while
                    setattr(passinfo, attr, result)
                    invalid_option = False

            if invalid_option:
                continue

            if passinfo.highcompsymb == None and passinfo.medcompsymb == None and passinfo.lowcompsymb == None:
                has_symbols = input("La contraseña tendrá símbolos? [S/N]: ")
                if has_symbols.lower() not in ["s", "n"]:
                    getpass("\nLa opción no es válida, presione ENTER para continuar.")
                    continue
                elif has_symbols.lower() == "n":
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

        #while True:
        #    password = password_generator(password_length, selected_charsets)
        #    if cumple_requisitos(password, selected_charsets):
        #        break

        password = password_generator(passinfo.length, selected_charsets)

        show_header("=== OPCIÓN 2: GENERADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")

        show_password_summary(passinfo)
        print("\nLa contraseña generada es: ", end=""); cprint(password, "G")
            
        try:
            getpass("\nPresione ENTER para volver al menú principal.")
        except KeyboardInterrupt:
            handle_program_exit()
    except KeyboardInterrupt:
        handle_task_stop()

# Bloque para prevenir la ejecución directa del módulo.
if __name__ == "__main__":
    cprint("\n[*] Este módulo no puede ser ejecutado directamente.\n", "R")