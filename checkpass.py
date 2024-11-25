"""
checkpass.py

Este módulo implementa la lógica principal del análisis de contraseñas, incluyendo la verificación
de sus características, cálculo de tiempos de ruptura por fuerza bruta y determinación de su nivel
de seguridad.
"""

import signal
import sys
from getpass import getpass

from modules import passutils
from modules.utils import clear_console, cprint, format_time, handle_task_stop, handle_program_exit
from modules.constants import DEFAULT_DEVICE_HASHRATE, PASSWORD_SECURITY_LIMITS

def show_header():
    """
    Limpia la consola y muestra el encabezado del analizador de contraseñas.
    """

    clear_console()
    cprint("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n", "Y")

def input_password():
    """
    Solicita al usuario una contraseña válida y la confirma.

    Returns:
        str: Contraseña válida ingresada por el usuario.
    """

    while True:
        show_header()
        password = getpass("Ingrese la contraseña a analizar: ")

        error_message = validate_password(password)
        if error_message:
            getpass(f"\n{error_message} presione ENTER para continuar.")
            continue

        repeat_pass = getpass("Ingrese nuevamente la contraseña: ")
        if password != repeat_pass:
            getpass("\nLas contraseñas no coinciden, presione ENTER para continuar.")
            continue

        return password

def validate_password(password):
    """
    Valida la contraseña y genera un mensaje de error en caso de que no sea válida.

    Args:
        password (str): Contraseña ingresada.

    Returns:
        str | None: Mensaje de error si la contraseña no es válida, None si es válida.
    """

    if not password:
        return "No ha ingresado una contraseña,"
    if " " in password:
        return "La contraseña no puede tener espacios,"
    if not passutils.is_password_vaild(password):
        return "La contraseña contiene caracteres inválidos,"
    return None

def analyze_password_props(password, passinfo):
    """
    Analiza las propiedades de una contraseña y actualiza la información en `passinfo`.

    Args:
        password (str): Contraseña a analizar.
        passinfo (PasswordInfo): Objeto donde se almacenan las propiedades de la contraseña.
    """

    chartypes = {
        "digits": passutils.DIGITS,
        "lower": passutils.LOWER,
        "upper": passutils.UPPER,
        "highcompsymb": passutils.HIGH_COMP_SYMB,
        "medcompsymb": passutils.MED_COMP_SYMB,
        "lowcompsymb": passutils.LOW_COMP_SYMB
    }

    passinfo.length = len(password)
    for key, chartype in chartypes.items():
        setattr(passinfo, key, passutils.password_has_chartype(password, chartype))

def show_password_summary(passinfo):
    """
    Muestra un resumen de las propiedades de la contraseña.

    Args:
        passinfo (PasswordInfo): Objeto con las propiedades de la contraseña.
    """

    print("Resumen de la contraseña ingresada:")
    cprint("[*] ", "Y", ""); print("Longitud: ", end=""); cprint(str(passinfo.length), "R") if passinfo.length <= 10 else cprint(str(passinfo.length), "G")
    cprint("[*] ", "Y", ""); print("Tiene números: ", end=""); cprint("Si", "G") if passinfo.digits else cprint("No", "R")
    cprint("[*] ", "Y", ""); print("Tiene letras minúsculas: ", end=""); cprint("Si", "G") if passinfo.lower else cprint("No", "R")
    cprint("[*] ", "Y", ""); print("Tiene letras mayúsculas: ", end=""); cprint("Si", "G") if passinfo.upper else cprint("No", "R")
    cprint("[*] ", "Y", ""); print("Tiene símbolos: ", end="")
    if passinfo.highcompsymb or passinfo.medcompsymb or passinfo.lowcompsymb:
        cprint("Si", "G")
        cprint("[*] ", "Y", ""); print("Compatibilidad de símbolos utilzados: ", end="")
        if passinfo.lowcompsymb:
            cprint("Baja", "R")
        elif passinfo.medcompsymb:
            cprint("Media", "C")
        else:
            cprint("Alta", "G")
    else:
        cprint("No", "R")

def confirm_bruteforce_analysis(passinfo):
    """
    Confirma si el usuario desea continuar con el análisis de seguridad por fuerza bruta.

    Args:
        passinfo (PasswordInfo): Objeto con las propiedades de la contraseña.

    Returns:
        bool: True si el usuario confirma, False si cancela.
    """

    while True:
        show_header()
        show_password_summary(passinfo)
        confirmation = input("\nDesea verificar la seguridad de su contraseña? [S/n]: ")
        if confirmation not in ["", "s", "S", "n", "N"]:
            getpass("\nOpción incorrecta, presione ENTER para continuar.")
            continue
        if confirmation in ["n", "N"]:
            getpass("\nVerificación cancelada, presione ENTER para volver al menú principal.")
            return False
        
        return True

def calc_password_combinations(passinfo):
    """
    Calcula el número total de combinaciones posibles según las propiedades de la contraseña.

    Args:
        passinfo (PasswordInfo): Objeto con las propiedades de la contraseña.

    Returns:
        int: Número total de combinaciones posibles.
    """

    charsets = [
        len(passutils.DIGITS) if passinfo.digits else 0,
        len(passutils.LOWER) if passinfo.lower else 0,
        len(passutils.UPPER) if passinfo.upper else 0,
        len(passutils.HIGH_COMP_SYMB) if passinfo.highcompsymb else 0,
        len(passutils.MED_COMP_SYMB) if passinfo.medcompsymb else 0,
        len(passutils.LOW_COMP_SYMB) if passinfo.lowcompsymb else 0,
    ]
    return sum(charsets) ** passinfo.length

def get_bruteforce_time(pass_combinations, hashrate):
    """
    Calcula el tiempo estimado para romper la contraseña mediante fuerza bruta.

    Args:
        pass_combinations (int): Número total de combinaciones posibles.
        hashrate (float): Velocidad del dispositivo en hashes por segundo.

    Returns:
        float: Tiempo estimado en segundos.
    """

    return pass_combinations/hashrate

def set_password_secururity(bruteforce_time, passinfo):
    """
    Determina el nivel de seguridad de la contraseña basado en el tiempo de ruptura estimado.

    Args:
        bruteforce_time (float): Tiempo estimado de ruptura en segundos.
        passinfo (PasswordInfo): Objeto con las propiedades de la contraseña.
    """

    if 0 <= bruteforce_time <= PASSWORD_SECURITY_LIMITS[0]:
        passinfo.security = 0
    elif PASSWORD_SECURITY_LIMITS[0] < bruteforce_time <= PASSWORD_SECURITY_LIMITS[1]:
        passinfo.security = 1
    elif PASSWORD_SECURITY_LIMITS[1] < bruteforce_time <= PASSWORD_SECURITY_LIMITS[2]:
        passinfo.security = 2
    elif PASSWORD_SECURITY_LIMITS[2] < bruteforce_time <= PASSWORD_SECURITY_LIMITS[3]:
        passinfo.security = 3
    else:
        passinfo.security = 4

def get_security_color(passinfo_security):
    """
    Asigna un color al mensaje basado en el nivel de seguridad.

    Args:
        passinfo_security (int): Nivel de seguridad (0 a 4).

    Returns:
        str: Código de color ANSI para el nivel de seguridad.
    """

    color_map = {0: "M", 1: "R", 2: "Y", 3: "C", 4: "G"}
    return color_map.get(passinfo_security, "RST")

def checkpass():
    """
    Punto de entrada principal para el análisis de contraseñas.

    Solicita una contraseña al usuario, analiza sus propiedades, calcula el tiempo de ruptura
    por fuerza bruta, determina el nivel de seguridad y muestra los resultados.

    Maneja interrupciones (Ctrl+C) y permite salir del programa de manera controlada.
    """

    try:
        password = input_password()
        passinfo = passutils.PasswordInfo()
        analyze_password_props(password, passinfo)

        if confirm_bruteforce_analysis(passinfo):
            num_passwords = calc_password_combinations(passinfo)
            pass_breaktime = get_bruteforce_time(num_passwords, DEFAULT_DEVICE_HASHRATE)
            breaktime_text = format_time(pass_breaktime)
            set_password_secururity(pass_breaktime, passinfo)
            breaktime_text_color = get_security_color(passinfo.security)

            print(f"Tiempo para romper la contraseña: ", end = ""); cprint(breaktime_text, breaktime_text_color)
            try:
                getpass("\nPresione ENTER para volver al menú principal.")
            except KeyboardInterrupt:
                handle_program_exit()

    except KeyboardInterrupt:
        handle_task_stop()
