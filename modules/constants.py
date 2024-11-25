APP_NAME = "pypasstool"
APP_VER = "0.1.0"

# Constantes de colores
COLORS = {
    "R": "\033[31m",
    "G": "\033[32m",
    "B": "\033[34m",
    "M": "\033[35m",
    "Y": "\033[33m",
    "C": "\033[36m",
    "RST": "\033[0m"
}

# Hardware hashrate
RTX4090_HASHES = {
    "BCRYPT": 1.84e5,
    "MD5": 1.641e11,
    "SHA-1": 5.06387e10
}

HASHRATE = {
    "RTX4090": RTX4090_HASHES
}

DEFAULT_HASHCALC = HASHRATE["RTX4090"]["MD5"]*12

LIMIT_TIMES = [
    1, 24*60*60, 7*24*60*60, 30*24*60*60
]