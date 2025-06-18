"""
checkpass.py

Este módulo implementa la lógica principal del análisis de contraseñas, incluyendo la verificación
de sus propiedades, cálculo de tiempos de ruptura por fuerza bruta y determinación de su nivel
de seguridad.
"""

from getpass import getpass

from models.checkpass import get_devices, get_device_hashes, find_password_props_id, insert_password_props, find_bruteforce_entry, insert_password_bruteforce, update_bruteforce_time

from utils import passutils
from utils.utils import clear_console, cprint, format_time, handle_task_stop, handle_program_exit, show_header
from utils.constants import PASSWORD_SECURITY_LIMITS

def show_password():
    """
    Solicita al usuario que indique si desea mostrar la contraseña en pantalla.

    Returns:
        None | bool: None si la respuesta no es válida, True si el usuario elige mostrar la contraseña,
                     False si el usuario elige no mostrar la contraseña.
    """

    show_password = input("Mostrar contraseña en pantalla? [S/N]: ")
    if show_password.lower() not in ["s", "n"]:
        getpass("\nOpción incorrecta, presione ENTER para continuar.")
        return None
    elif show_password.lower() == "s":
        return True
    else:
        return False

def select_bruteforce_device(db_conn):
    """
    Permite al usuario elegir un dispositivo de la tabla devices en la base de datos.

    Args:
        db_conn: Conexión a la base de datos.

    Returns:
        dict: None si la respuesta no es válida, o un diccionario con id_dev y dev_name.
    """

    devices = get_devices(db_conn)
    
    print("Seleccione el dispositivo para el análisis de fuerza bruta:\n")
    for opt, (id_dev, dev_name) in enumerate(devices, 1):
        print(f"{opt}. {dev_name}")

    option = input("\nDispositivo seleccionado: ")
    if option.isdigit() and 1 <= int(option) <= len(devices):
        id_dev, dev_name = devices[int(option) - 1]
        return {"id_dev": id_dev, "dev_name": dev_name}
    else:
        getpass("\nOpción incorrecta, presione ENTER para continuar.")
        return None

def select_device_hash(db_conn, id_dev):
    """
    Permite al usuario elegir un algoritmo de hash disponible para el dispositivo seleccionado
    y retorna el valor de hashes por segundo (hashrate) correspondiente.

    Args:
        db_conn: Conexión a la base de datos.
        id_dev (int): ID del dispositivo seleccionado.

    Returns:
        dict | None: Diccionario con id_algo y device_hashrate, o None si la opción es inválida.
    """

    hashes = get_device_hashes(db_conn, id_dev)

    print("Seleccione el algoritmo de hash para el análisis de fuerza bruta:\n")
    for hash, (id_algo, algo_name, hashrate) in enumerate(hashes, 1):
        print(f"{hash}. {algo_name} ({hashrate:.2e} hashes/seg)")

    option = input("\nHash seleccionado: ")
    if option.isdigit() and 1 <= int(option) <= len(hashes):
        id_algo, algo_name, hashrate = hashes[int(option) - 1]
        return {"id_algo": id_algo, "algo_name": algo_name, "device_hashrate": hashrate}
    else:
        getpass("\nOpción incorrecta, presione ENTER para continuar.")
        return None

def analyze_password_props(password, passinfo):
    """
    Analiza las propiedades de una contraseña y actualiza la información en `passinfo`.

    Args:
        password (str): Contraseña a analizar.
        passinfo (PasswordInfo): Objeto donde se almacenan las propiedades de la contraseña.
    """

    chartypes = {
        "digits": passutils.DIGITS,
        "lower": passutils.LOWER,
        "upper": passutils.UPPER,
        "highcompsymb": passutils.HIGH_COMP_SYMB,
        "medcompsymb": passutils.MED_COMP_SYMB,
        "lowcompsymb": passutils.LOW_COMP_SYMB
    }

    passinfo.length = len(password)
    for key, chartype in chartypes.items():
        setattr(passinfo, key, passutils.password_has_chartype(password, chartype))

def confirm_bruteforce_analysis(passinfo, device, hashrate):
    """
    Confirma si el usuario desea continuar con el análisis de seguridad de la contraseña
    por fuerza bruta.

    Args:
        passinfo (PasswordInfo): Objeto con las propiedades de la contraseña.

    Returns:
       None | bool: None si la respuesta no es válida, True si el usuario confirma, False si cancela.
    """

    passutils.show_password_summary(passinfo)
    print("\nInformación del análisis de fuerza bruta:")
    cprint("[*] ", "Y", ""); print(f"Dispositivo seleccionado: {device['dev_name']}")
    cprint("[*] ", "Y", ""); print(f"Algoritmo de hasheo: {hashrate['algo_name']}")
    confirmation = input("\nDesea verificar la seguridad de su contraseña? [S/N]: ")
    if confirmation.lower() not in ["s", "n"]:
        getpass("\nOpción incorrecta, presione ENTER para continuar.")
        return None
    if confirmation.lower() == "n":
        getpass("\nVerificación cancelada, presione ENTER para volver al menú principal.")
        return False
    
    return True

def process_bruteforce_entry(db_conn, passinfo, pwd_props_id, bruteforce_device, device_hashrate):
    """
    Inserta una nueva entrada en password_bruteforce para la combinación dada y calcula el tiempo de ruptura.

    Args:
        db_conn: Conexión a la base de datos.
        passinfo: Objeto PasswordInfo con las propiedades de la contraseña.
        pwd_props_id (int): ID de las propiedades de la contraseña.
        bruteforce_device (dict): Diccionario con info del dispositivo seleccionado.
        device_hashrate (dict): Diccionario con info del hash seleccionado.
    """
    insert_password_bruteforce(db_conn, pwd_props_id, bruteforce_device["id_dev"], device_hashrate["id_algo"])
    num_passwords = calc_password_combinations(passinfo)
    pass_breaktime = calc_bruteforce_time(num_passwords, device_hashrate["device_hashrate"])
    update_bruteforce_time(db_conn, pwd_props_id, bruteforce_device["id_dev"], device_hashrate["id_algo"], pass_breaktime)
    return pass_breaktime

def calc_password_combinations(passinfo):
    """
    Calcula el número total de combinaciones posibles según las propiedades de la contraseña.

    Args:
        passinfo (PasswordInfo): Objeto con las propiedades de la contraseña.

    Returns:
        int: Número total de combinaciones posibles.
    """

    charsets = [
        len(passutils.DIGITS) if passinfo.digits else 0,
        len(passutils.LOWER) if passinfo.lower else 0,
        len(passutils.UPPER) if passinfo.upper else 0,
        len(passutils.HIGH_COMP_SYMB) if passinfo.highcompsymb else 0,
        len(passutils.HIGH_COMP_SYMB) + len(passutils.MED_COMP_SYMB) if passinfo.medcompsymb else 0,
        len(passutils.HIGH_COMP_SYMB) + len(passutils.MED_COMP_SYMB) + len(passutils.LOW_COMP_SYMB) if passinfo.lowcompsymb else 0,
    ]

    return sum(charsets) ** passinfo.length

def calc_bruteforce_time(pass_combinations, hashrate):
    """
    Calcula el tiempo estimado para romper la contraseña mediante fuerza bruta.

    Args:
        pass_combinations (int): Número total de combinaciones posibles.
        hashrate (float): Velocidad del dispositivo en hashes por segundo.

    Returns:
        float: Tiempo estimado en segundos.
    """

    return pass_combinations/hashrate

def set_password_security(bruteforce_time, passinfo):
    """
    Determina el nivel de seguridad de la contraseña basado en el tiempo de ruptura estimado.

    Args:
        bruteforce_time (float): Tiempo estimado de ruptura en segundos.
        passinfo (PasswordInfo): Objeto con las propiedades de la contraseña.
    """

    if 0 <= bruteforce_time <= PASSWORD_SECURITY_LIMITS[0]:
        passinfo.security = 0
    elif PASSWORD_SECURITY_LIMITS[0] < bruteforce_time <= PASSWORD_SECURITY_LIMITS[1]:
        passinfo.security = 1
    elif PASSWORD_SECURITY_LIMITS[1] < bruteforce_time <= PASSWORD_SECURITY_LIMITS[2]:
        passinfo.security = 2
    elif PASSWORD_SECURITY_LIMITS[2] < bruteforce_time <= PASSWORD_SECURITY_LIMITS[3]:
        passinfo.security = 3
    else:
        passinfo.security = 4

def get_security_color(passinfo_security):
    """
    Asigna un color al mensaje basado en el nivel de seguridad.

    Args:
        passinfo_security (int): Nivel de seguridad (0 a 4).

    Returns:
        str: Código de color ANSI para el nivel de seguridad.
    """

    color_map = {0: "M", 1: "R", 2: "Y", 3: "C", 4: "G"}
    return color_map.get(passinfo_security, "RST")

def password_improvements(passinfo):
    """
    Genera sugerencias para mejorar la seguridad de la contraseña en base a sus propiedades
    y nivel de seguridad.

    Args:
        passinfo (PasswordInfo): Objeto con las propiedades de la contraseña.

    Returns:
        improvements_list (list[str]): Lista de sugerencias para mejorar la contraseña.
    """
    improvements_list = []

    if passinfo.security == 4:
        improvements_list.append("Tu contraseña es muy segura. ¡Buen trabajo!")
    else:
        if passinfo.security == 0:
            improvements_list.append("Tu contraseña es extremadamente débil a ataques de fuerza bruta. Considera cambiarla de inmediato.")
        elif passinfo.security == 1:
            improvements_list.append("Tu contraseña es muy débil a ataques de fuerza bruta. Se recomienda mejorarla para mayor seguridad.")
        elif passinfo.security == 2:
            improvements_list.append("Tu contraseña es débil a ataques de fuerza bruta. debería mejorarse.")
        elif passinfo.security == 3:
            improvements_list.append("Tu contraseña es fuerte a ataques de fuerza bruta, pero puedes hacerla más segura.")

        if passinfo.length < 12:
            improvements_list.append("Aumenta la longitud de tu contraseña. Se recomienda al menos 12 caracteres.")
        if not passinfo.digits:
            improvements_list.append("Incluye números en tu contraseña para mayor variedad.")
        if not passinfo.lower:
            improvements_list.append("Incluye letras minúsculas en tu contraseña.")
        if not passinfo.upper:
            improvements_list.append("Incluye letras mayúsculas en tu contraseña.")
        if not (passinfo.highcompsymb or passinfo.medcompsymb or passinfo.lowcompsymb):
            improvements_list.append("Agrega símbolos (como @, #, $, etc.) para aumentar la complejidad.")

    return improvements_list

def show_bruteforce_summary(improvements_list, breaktime_text, breaktime_text_color):
    """
    Muestra un resumen del análisis de fuerza bruta para la contraseña, incluyendo el tiempo estimado 
    para romperla y sugerencias de mejora.

    Args:
        improvements_list (list[str]): Lista de sugerencias para mejorar la seguridad de la contraseña.
        breaktime_text (str): Texto formateado que representa el tiempo estimado para romper la contraseña.
        breaktime_text_color (str): Código de color ANSI para mostrar el tiempo estimado con formato.
    """

    print("Resultados del análisis:")
    cprint("[*] ", "Y", ""); print(f"Tiempo para romper la contraseña: ", end = ""); cprint(breaktime_text, breaktime_text_color)
    for improvement in improvements_list:
        cprint("[*] ", "Y", ""); print(improvement)

def checkpass(db_conn):
    """
    Punto de entrada principal para el análisis de contraseñas.

    Solicita una contraseña al usuario, analiza sus propiedades, calcula el tiempo de ruptura
    por fuerza bruta, determina el nivel de seguridad y muestra los resultados.

    Maneja interrupciones (Ctrl+C) y permite salir del programa de manera controlada.
    """

    try:
        password_visible = None
        while password_visible == None:
            show_header("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            print("Este módulo le permitirá analizar la seguridad de su contraseña")
            print("contra ataques de fuerza bruta.\n")
            print("La contraseña no será mostrada en pantalla a menos que así lo desee.\n")
            password_visible = show_password()

        password = None
        while password == None:
            show_header("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            password = passutils.input_password(password_visible)
        
        bruteforce_device = None
        while bruteforce_device == None:
            show_header("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            bruteforce_device = select_bruteforce_device(db_conn)

        device_hashrate = None
        while device_hashrate == None:
            show_header("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            device_hashrate = select_device_hash(db_conn, bruteforce_device["id_dev"])

        passinfo = passutils.PasswordInfo()
        analyze_password_props(password, passinfo)

        confirmation = None
        while confirmation == None:
            show_header("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            confirmation = confirm_bruteforce_analysis(passinfo, bruteforce_device, device_hashrate)

        if confirmation:
            pwd_props_id = find_password_props_id(db_conn, passinfo)
            if not pwd_props_id:
                pwd_props_id = insert_password_props(db_conn, passinfo)
                pass_breaktime = process_bruteforce_entry(db_conn, passinfo, pwd_props_id, bruteforce_device, device_hashrate)
            else:
                bruteforce_entry = find_bruteforce_entry(db_conn, pwd_props_id, bruteforce_device["id_dev"], device_hashrate["id_algo"])
                if bruteforce_entry:
                    pass_breaktime = bruteforce_entry["bruteforce_time"]
                else:
                    pass_breaktime = process_bruteforce_entry(db_conn, passinfo, pwd_props_id, bruteforce_device, device_hashrate)
            breaktime_text = format_time(pass_breaktime)
            set_password_security(pass_breaktime, passinfo)
            breaktime_text_color = get_security_color(passinfo.security)
            improvements_list = password_improvements(passinfo)

            show_header("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            show_bruteforce_summary(improvements_list, breaktime_text, breaktime_text_color)
            try:
                getpass("\nPresione ENTER para volver al menú principal.")
            except KeyboardInterrupt:
                handle_program_exit()

    except KeyboardInterrupt:
        handle_task_stop()

# Bloque para prevenir la ejecución directa del módulo.
if __name__ == "__main__":
    cprint("\n[*] Este módulo no puede ser ejecutado directamente.\n", "R")