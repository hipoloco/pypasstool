import os
from modules.constants import COLORS

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def cprint(text, color):
    if not isinstance(text, str):
        raise ValueError("El texto a imprimir debe ser un string.")

    if not isinstance(color, str):
        raise ValueError("El color debe ser un string en mayúsculas.")
    
    # Usar el color por defecto si no se encuentra el color solicitado
    color = COLORS.get(color, COLORS.get("RST"))
    print(f"{color}{text}{COLORS['RST']}")