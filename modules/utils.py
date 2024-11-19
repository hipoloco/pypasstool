import os

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def cprint(text, color):
    """
    Imprime texto en el color especificado si es válido en el diccionario interno de colores.
    Si el color no se encuentra, usa el color por defecto.
    """

    if not isinstance(text, str):
        raise ValueError("El texto a imprimir debe ser un string.")

    if not isinstance(color, str):
        raise ValueError("El color debe ser un string en mayúsculas.")
    
    # Usar el color por defecto si no se encuentra el color solicitado
    color_to_use = color_dict.get(color, color_dict.get(default_color, ""))
    print(f"{color_to_use}{text}{color_dict['RESET']}")
