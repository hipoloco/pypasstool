"""
constants.py

Este módulo contiene todas las constantes utilizadas en la aplicación `pypasstool`. 
Incluye configuraciones generales, constantes de color, valores de hashrate para cálculos de contraseñas y límites para evaluar la seguridad.
"""

# Nombre y versión de la aplicación
APP_NAME = "pypasstool"
APP_VER = "1.1.0"

# Nombre de la base de datos SQLite
DATABASE_NAME = "pypasstool.db"

# Constantes de colores para uso en salida de consola con la función cprint
ANSI_COLORS = {
    "R": "\033[31m",
    "G": "\033[32m",
    "B": "\033[34m",
    "M": "\033[35m",
    "Y": "\033[33m",
    "C": "\033[36m",
    "RST": "\033[0m"
}

DEVICES = {
    "RTX 4090": {
        "dev_name": "RTX 4090",
        "hashrates": {
            "BCRYPT": 1.84e5,
            "MD5": 1.641e11,
            "SHA-1": 5.06387e10
        }
    },
    "RTX 4090 x 12": {
        "dev_name": "RTX 4090 x 12",
        "hashrates": {
            "BCRYPT": 1.84e5 * 12,
            "MD5": 1.641e11 * 12,
            "SHA-1": 5.06387e10 * 12
        }
    }
}

# Límites en segundos para clasificar la seguridad de una contraseña (ruptura por fuerza bruta)
# Categorías:
# - 0 a 1 segundo: Extremadamente débil
# - Hasta 1 día (24*60*60): Muy débil
# - Hasta 1 semana (7*24*60*60): Débil
# - Hasta 1 mes (30*24*60*60): Fuerte
# - Más de 1 mes: Muy fuerte
PASSWORD_SECURITY_LIMITS = [
    1,                # 1 segundo
    24 * 60 * 60,     # 1 día
    7 * 24 * 60 * 60, # 1 semana
    30 * 24 * 60 * 60 # 1 mes
]