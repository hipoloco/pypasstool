import os, sys
from getpass import getpass

from modules.constants import COLORS

def signal_handler_return():
    cprint("\n\n[*] Tarea interrumpida, presione ENTER para voler al menú principal.", "C", "")
    try:
        getpass("")
    except KeyboardInterrupt:
        signal_handler_exit()

def signal_handler_exit():
    cprint("\n\n[*] Programa interrumpido, saliendo de manera controlada...\n", "R")
    sys.exit(0)

""" def signal_handler_exit(sig, frame):
    signal_handler_exit_text() """

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def cprint(text, color, end="\n"):
    if not isinstance(text, str):
        raise ValueError("El texto a imprimir debe ser un string.")

    if not isinstance(color, str):
        raise ValueError("El color debe ser un string en mayúsculas.")
    
    # Usar el color por defecto si no se encuentra el color solicitado
    color = COLORS.get(color, COLORS.get("RST"))
    print(f"{color}{text}{COLORS['RST']}", end=end)

def secs_to_time(seconds):
    # Definición de las conversiones en segundos
    SECOND = 1
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 30 * DAY  # Aproximación de 1 mes = 30 días
    YEAR = 365 * DAY  # Aproximación de 1 año = 365 días

    if seconds < SECOND:
        return "Instantáneo"
    elif seconds < MINUTE:
        duration = int(seconds)
        unit = "segundo" if duration == 1 else "segundos"
        return f"{duration} {unit}"
    elif seconds < HOUR:
        duration = int(seconds // MINUTE)
        unit = "minuto" if duration == 1 else "minutos"
        return f"{duration} {unit}"
    elif seconds < DAY:
        duration = int(seconds // HOUR)
        unit = "hora" if duration == 1 else "horas"
        return f"{duration} {unit}"
    elif seconds < MONTH:
        duration = int(seconds // WEEK)
        unit = "semana" if duration == 1 else "semanas"
        return f"{duration} {unit}"
    elif seconds < YEAR:
        duration = int(seconds // MONTH)
        unit = "mes" if duration == 1 else "meses"
        return f"{duration} {unit}"
    else:
        duration_years = seconds / YEAR
        if duration_years >= 1e18:
            duration = duration_years / 1e18
            suffix = "T"
        elif duration_years >= 1e12:
            duration = duration_years / 1e12
            suffix = "B"
        elif duration_years >= 1e6:
            duration = duration_years / 1e6
            suffix = "M"
        else:
            duration = int(duration_years)
            suffix = ""
            
        unit = "año" if duration == 1 else "años"
        if suffix == "":
            return f"{duration} {unit}"
        else:
            return f"{duration:.2f}{suffix} {unit}"
