"""
constants.py

Este módulo contiene todas las constantes utilizadas en la aplicación `pypasstool`. 
Incluye configuraciones generales, constantes de color, valores de hashrate para cálculos de contraseñas y límites para evaluar la seguridad.
"""

# Nombre y versión de la aplicación
APP_NAME = "pypasstool"
APP_VER = "0.9.1"

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

# Hasrate (velocidades de procesamiento) para dispositivos específicos
HASHRATES_RTX4090 = {
    "BCRYPT": 1.84e5,
    "MD5": 1.641e11,
    "SHA-1": 5.06387e10
}

# Diccionario para agregar otros dispositivos en el futuro
DEVICE_HASHRATES = {
    "RTX4090": HASHRATES_RTX4090
}

# Hasrate por defecto para calcular tiempos de ruptura de contraseñas
DEFAULT_DEVICE_HASHRATE = DEVICE_HASHRATES["RTX4090"]["MD5"]*12 # Simula 12 dispositivos RTX 4090

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