"""
passutils.py

Este módulo contiene utilidades relacionadas con el análisis y validación de contraseñas.
Proporciona constantes para clasificar tipos de caracteres, funciones para analizar las 
características de una contraseña, para mostrar un resumen de las características de la
contraseña y una clase para almacenar información sobre contraseñas.
"""

from getpass import getpass
# pip install git+https://github.com/binbash23/pwinput.git
# Para resolver el uso de Ctrl+C (https://github.com/asweigart/pwinput/pull/7)
from pwinput import pwinput # type: ignore

from modules.utils import cprint

# Conjuntos de caracteres clasificados por compatibilidad
HIGH_COMP_SYMB = set([
    "!", "#", "$", "%", "&", "*", "@", "^"
])  # Símbolos altamente compatibles

MED_COMP_SYMB = set([
    "(", ")", "-", ".", "_"
])  # Símbolos moderadamente compatibles

LOW_COMP_SYMB = set([
    '"', "'", "+", ",", "/", ":", ";", "<", "=", ">", "?", "[", "\\", "]", "`", "{", "|", "}", "~"
])  # Símbolos menos compatibles

DIGITS = set([
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
])  # Caracteres numéricos

LOWER = set([
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
])  # Letras minúsculas

UPPER = set([
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
])  # Letras mayúsculas

# Conjunto de caracteres válidos para contraseñas
VALID_PASS_CHARS = (LOW_COMP_SYMB | MED_COMP_SYMB | HIGH_COMP_SYMB | DIGITS | LOWER | UPPER)

def password_has_chartype(password, char_list):
    """
    Verifica si la contraseña contiene al menos un carácter de un conjunto específico.

    Args:
        password (str): Contraseña a analizar.
        char_list (set): Conjunto de caracteres a buscar.

    Returns:
        bool: True si al menos un carácter está presente, False en caso contrario.
    """
    return any(char in char_list for char in password)

def is_password_vaild(password):
    """
    Comprueba si todos los caracteres de la contraseña pertenecen al conjunto permitido de caracteres.

    Args:
        password (str): Contraseña a validar.

    Returns:
        bool: True si todos los caracteres son válidos, False en caso contrario.
    """
    return all(char in VALID_PASS_CHARS for char in password)

def input_password(show_password = False):
    """
    Solicita al usuario una contraseña válida y en caso de ser necesario, la confirma.

    Args:
        show_password (bool): Determina si la contraseña será visible mientras se ingresa.

    Returns:
        None | str: None si la contraseña no es válida, contraseña si es válida y confirmada.
    """

    if show_password == False:
        password = pwinput("Ingrese la contraseña: ", "*")
    else:
        password = input("Ingrese la contraseña: ")

    error_message = validate_password(password)
    if error_message:
        getpass(f"\n{error_message} presione ENTER para continuar.")
        return None

    if show_password == False:
        repeat_pass = pwinput("Ingrese nuevamente la contraseña: ", "*")
        if password != repeat_pass:
            getpass("\nLas contraseñas no coinciden, presione ENTER para continuar.")
            return None

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
    if not is_password_vaild(password):
        return "La contraseña contiene caracteres inválidos,"
    return None

def show_password_summary(passinfo):
    """
    Muestra un resumen de las propiedades de la contraseña.

    Args:
        passinfo (PasswordInfo): Objeto con las propiedades de la contraseña.
    """

    print("Resumen de la contraseña:")
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

class PasswordInfo:
    """
    Clase que almacena información sobre las propiedades de una contraseña.

    Atributos:
        length (int): Longitud de la contraseña.
        digits (bool): Indica si contiene números.
        lower (bool): Indica si contiene letras minúsculas.
        upper (bool): Indica si contiene letras mayúsculas.
        highcompsymb (bool): Indica si contiene símbolos altamente compatibles.
        medcompsymb (bool): Indica si contiene símbolos moderadamente compatibles.
        lowcompsymb (bool): Indica si contiene símbolos poco compatibles.
        security (int): Nivel de seguridad asignado a la contraseña.
    """
    def __init__(self):
        self.length = None
        self.digits = None
        self.lower = None
        self.upper = None
        self.highcompsymb = None
        self.medcompsymb = None
        self.lowcompsymb = None
        self.security = None

# Bloque para prevenir la ejecución directa del módulo.
if __name__ == "__main__":
    cprint("\n[*] Este módulo no puede ser ejecutado directamente.\n", "R")