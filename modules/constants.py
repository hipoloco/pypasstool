APP_NAME = "pypasstool"
VERSION = "0.0.1"

# Constantes de colores
COLORS = {
    "R": "\033[31m",
    "G": "\033[32m",
    "B": "\033[34m",
    "Y": "\033[33m",
    "RST": "\033[0m"
}

# Hardware hashrate
RTX4090 = {
    "BCRYPT": 1.84e5,
    "MD5": 1.641e11,
    "SHA-1": 5.06387e10
}

HASHRATE = {
    "RTX4090": RTX4090
}

DEFAULT_HASHCALC = HASHRATE["RTX4090"]["MD5"]