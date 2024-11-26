"""
passutils.py

Este módulo contiene utilidades relacionadas con el análisis y validación de contraseñas.
Proporciona constantes para clasificar tipos de caracteres, funciones para analizar las características de una contraseña, 
y una clase para almacenar información sobre su seguridad.
"""

from getpass import getpass

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

def input_password():
    """
    Solicita al usuario una contraseña válida y la confirma.

    Returns:
        None | str: None si la contraseña no es válida, contraseña si es válida y confirmada.
    """

    password = getpass("Ingrese la contraseña a analizar: ")

    error_message = validate_password(password)
    if error_message:
        getpass(f"\n{error_message} presione ENTER para continuar.")
        return None

    repeat_pass = getpass("Ingrese nuevamente la contraseña: ")
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
        self.length = 0
        self.digits = False
        self.lower = False
        self.upper = False
        self.highcompsymb = False
        self.medcompsymb = False
        self.lowcompsymb = False
        self.security = 0