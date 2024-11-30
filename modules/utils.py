"""
utils.py

Este módulo proporciona funciones utilitarias para gestionar señales, limpiar la pantalla, 
imprimir cabezeras, imprimir con colores personalizados y convertir segundos a unidades 
de tiempo legibles. Estas funciones son de uso común en la aplicación para mejorar
la interacción del usuario.
"""

import os
import sys
from getpass import getpass

from modules.constants import ANSI_COLORS, APP_NAME

def handle_task_stop():
    """
    Maneja una interrupción (Ctrl+C) durante una tarea y permite al usuario volver al menú principal.

    Muestra un mensaje de interrupción y espera a que el usuario presione ENTER.
    Si se interrumpe nuevamente (Ctrl+C), llama a signal_handler_exit() para salir del programa.
    """
    cprint("\n\n[*] Tarea interrumpida, presione ENTER para voler al menú principal.", "C", "")
    try:
        getpass("")
    except KeyboardInterrupt:
        handle_program_exit()

def handle_program_exit():
    """
    Maneja una interrupción (Ctrl+C) global del programa y realiza una salida controlada.

    Muestra un mensaje en rojo indicando que el programa ha sido interrumpido y termina la ejecución.
    """
    cprint(f"\n\n[*] Programa interrumpido, saliendo de {APP_NAME} de manera controlada.\n", "R")
    sys.exit(0)

def clear_console():
    """
    Limpia la consola dependiendo del sistema operativo.

    Para sistemas Windows utiliza `cls`.
    Para otros sistemas (Linux/Mac) utiliza `clear`.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def cprint(text, color, end="\n"):
    """
    Imprime texto con colores personalizados utilizando los códigos definidos en `ANSI_COLORS`.

    Args:
        text (str): El texto a imprimir.
        color (str): La clave del color en el diccionario `ANSI_COLORS` (ej. "R" para rojo).
        end (str, opcional): El carácter que se imprime al final. Por defecto es un salto de línea.
    """
    
    # Usar el color por defecto si no se encuentra el color solicitado
    color = ANSI_COLORS.get(color, ANSI_COLORS.get("RST"))
    print(f"{color}{text}{ANSI_COLORS['RST']}", end=end)

def format_time(seconds):
    """
    Convierte segundos a una representación legible en diferentes unidades de tiempo.

    La conversión incluye:
    - Segundos, minutos, horas, días, semanas, meses, años.
    - Para grandes cantidades de años, utiliza sufijos (M = millones, B = billones, T = trillones).

    Args:
        seconds (float): Cantidad de segundos a convertir.

    Returns:
        str: Representación legible de la duración en tiempo.
    """

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

def show_header(message):
    """
    Limpia la consola y muestra el encabezado del analizador de contraseñas.

    Args:
        message (str): Mensaje a mostrar en el encabezado.
    """

    clear_console()
    cprint(message, "Y")

# Bloque para prevenir la ejecución directa del módulo.
if __name__ == "__main__":
    cprint("\n[*] Este módulo no puede ser ejecutado directamente.\n", "R")