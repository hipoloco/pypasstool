"""
passgenerator.py

Este módulo permite generar contraseñas basadas en los requisitos definidos por el usuario.
El usuario puede especificar el largo de la contraseña, los conjuntos de caracteres permitidos 
(números, letras mayúsculas, letras minúsculas y símbolos), y el nivel de compatibilidad de los
símbolos.
"""

import time
from getpass import getpass
from models.passgenerator import find_password
from models.common import insert_password
from utils import passutils
from utils.utils import cprint, handle_task_stop, handle_program_exit, show_header

def password_generator(db_conn, length, charset_list):
    """
    Genera una contraseña basada en el largo especificado y los conjuntos de caracteres seleccionados.

    Args:
        db_conn: Conexión a la base de datos.
        length (int): Largo de la contraseña a generar.
        charset_list (list[list[str]]): Lista de conjuntos de caracteres permitidos.

    Returns:
        str: Contraseña generada que cumple con los requisitos.
    """
    # Crear un único string con todos los caracteres permitidos
    allchars = ''.join(''.join(charset) for charset in charset_list)

    # Generar contraseña utilizando un generador pseudoaleatorio basado en tiempo
    password = ""
    seed = int(time.time() * 1000)  # Usar el tiempo actual como semilla
    for i in range(length):
        seed = (seed * 9301 + 49297) % 233280
        index = seed % len(allchars)
        password += allchars[index]

    # Verificar que la contraseña cumpla con los requisitos de todos los conjuntos de caracteres
    if all(any(char in charset for char in password) for charset in charset_list):
        hashedpass = passutils.hash_password(password)
        if find_password(db_conn, hashedpass):
            return password_generator(db_conn, length, charset_list)
        else:
            insert_password(db_conn, hashedpass)
            return password
    else:
        return password_generator(db_conn, length, charset_list)  # Intentar nuevamente

def set_password_length():
    """
    Solicita al usuario el largo de la contraseña.

    Returns:
        None | int: Largo ingresado por el usuario o None si la entrada no es válida.
    """
    password_length = input("Ingresar el largo de la contraseña a generar (12-30): ")
    if not password_length.isdigit():
        getpass("\nLo ingresado no es un número, presione ENTER para continuar.")
        return None

    password_length = int(password_length)
    if password_length < 12 or password_length > 30:
        getpass("\nLa contraseña debe tener entre 12 y 30 caracteres, presione ENTER para continuar.")
        return None

    return password_length

def ask_yes_no(question):
    """
    Solicita al usuario una respuesta afirmativa o negativa (S/N).

    Args:
        question (str): Pregunta que se mostrará al usuario.

    Returns:
        None | bool: True si la respuesta es afirmativa, False si es negativa, None si es inválida.
    """
    answer = input(f"{question} [S/N]: ")
    if answer.lower() not in ['s', 'n']:
        input("\nLa opción no es válida, presione ENTER para continuar.")
        return None
    return answer.lower() == 's'

def passgenerator(db_conn):
    """
    Punto de entrada principal para el generador de contraseñas.

    Solicita al usuario los requisitos de la contraseña, genera una contraseña segura
    y la muestra al usuario. Garantiza que la contraseña cumpla con todos los requisitos.

    Maneja interrupciones (Ctrl+C) y permite salir del programa de manera controlada.
    """
    try:
        passinfo = passutils.PasswordInfo()
        finishPassInfo = False
        while not finishPassInfo:
            show_header("=== OPCIÓN 2: GENERADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")

            # Solicitar el largo de la contraseña
            if passinfo.length is None:
                passinfo.length = set_password_length()
                if passinfo.length is None:
                    continue

            # Solicitar requisitos de la contraseña
            options = [
                ('digits', 'La contraseña tendrá números?'),
                ('lower', 'La contraseña tendrá letras minúsculas?'),
                ('upper', 'La contraseña tendrá letras mayúsculas?')
            ]

            invalid_option = False # Flag para determinar si es necesario iterar nuevamente en el bucle principal
            for attr, question in options:
                if getattr(passinfo, attr) is None:
                    result = ask_yes_no(question)
                    if result is None:
                        invalid_option = True
                        break
                    setattr(passinfo, attr, result)

            # Si hubo un break en el bucle for anterior, vuelvo a iterar sobre el bucle principal
            if invalid_option:
                continue

            # Preguntar sobre símbolos y su compatibilidad
            if passinfo.highcompsymb is None and passinfo.medcompsymb is None and passinfo.lowcompsymb is None:
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

        # Construir la lista de conjuntos de caracteres seleccionados
        all_charsets = [
            passutils.DIGITS if passinfo.digits else None,
            passutils.LOWER if passinfo.lower else None,
            passutils.UPPER if passinfo.upper else None,
            passutils.HIGH_COMP_SYMB if passinfo.highcompsymb else None,
            passutils.MED_COMP_SYMB if passinfo.medcompsymb else None,
            passutils.LOW_COMP_SYMB if passinfo.lowcompsymb else None,
        ]
        selected_charsets = [charset for charset in all_charsets if charset is not None]

        # Generar contraseña
        password = password_generator(db_conn, passinfo.length, selected_charsets)

        # Mostrar el resultado
        show_header("=== OPCIÓN 2: GENERADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
        passutils.show_password_summary(passinfo)
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
