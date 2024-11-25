import signal, sys
from getpass import getpass

from modules import passutils
from modules.utils import clear_screen, cprint, secs_to_time, signal_handler_return, signal_handler_exit
from modules.constants import DEFAULT_HASHCALC, LIMIT_TIMES

def header():
    clear_screen()
    cprint("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n", "Y")

def get_password():
    while True:
        header()
        password = getpass("Ingrese la contraseña a analizar: ")

        error_message = validate_password_message(password)
        if error_message:
            getpass(f"\n{error_message} presione ENTER para continuar.")
            continue

        repeat_pass = getpass("Ingrese nuevamente la contraseña: ")
        if password != repeat_pass:
            getpass("\nLas contraseñas no coinciden, presione ENTER para continuar.")
            continue

        return password

def validate_password_message(password):
    if not password:
        return "No ha ingresado una contraseña,"
    if " " in password:
        return "La contraseña no puede tener espacios,"
    if not passutils.validate_password(password):
        return "La contraseña contiene caracteres inválidos,"
    return None

def analyze_password(password, passinfo):
    chartypes = {
        "number": passutils.NUMS,
        "lowercase": passutils.LOWER,
        "uppercase": passutils.UPPER,
        "secsymbol": passutils.SEC_SYMB,
        "commsymbol": passutils.COMM_SYMB,
        "qwertysymbol": passutils.QWERTY_SYMB
    }

    passinfo.length = len(password)
    for key, chartype in chartypes.items():
        setattr(passinfo, key, passutils.pass_has_chartype(password, chartype))

def resume_password(passinfo):
    print("Resumen de la contraseña ingresada:")
    cprint("[*] ", "Y", ""); print("Longitud: ", end=""); cprint(str(passinfo.length), "R") if passinfo.length <= 10 else cprint(str(passinfo.length), "G")
    cprint("[*] ", "Y", ""); print("Tiene números: ", end=""); cprint("Si", "G") if passinfo.number else cprint("No", "R")
    cprint("[*] ", "Y", ""); print("Tiene letras minúsculas: ", end=""); cprint("Si", "G") if passinfo.lowercase else cprint("No", "R")
    cprint("[*] ", "Y", ""); print("Tiene letras mayúsculas: ", end=""); cprint("Si", "G") if passinfo.uppercase else cprint("No", "R")
    cprint("[*] ", "Y", ""); print("Tiene símbolos: ", end="")
    if passinfo.secsymbol or passinfo.commsymbol or passinfo.qwertysymbol:
        cprint("Si", "G")
        cprint("[*] ", "Y", ""); print("Compatibilidad de símbolos utilzados: ", end="")
        if passinfo.qwertysymbol:
            cprint("Baja", "R")
        elif passinfo.commsymbol:
            cprint("Media", "C")
        else:
            cprint("Alta", "G")
    else:
        cprint("No", "R")

def analyze_password_bruteforce(passinfo):
    while True:
        header()
        resume_password(passinfo)
        confirmation = input("\nDesea verificar la seguridad de su contraseña? [S/n]: ")
        if confirmation not in ["", "s", "S", "n", "N"]:
            getpass("\nOpción incorrecta, presione ENTER para continuar.")
            continue
        if confirmation in ["n", "N"]:
            getpass("\nVerificación cancelada, presione ENTER para volver al menú principal.")
            return False
        
        return True

def calc_passwords(passinfo):
    charsets = [
        len(passutils.NUMS) if passinfo.number else 0,
        len(passutils.LOWER) if passinfo.lowercase else 0,
        len(passutils.UPPER) if passinfo.uppercase else 0,
        len(passutils.SEC_SYMB) if passinfo.secsymbol else 0,
        len(passutils.COMM_SYMB) if passinfo.commsymbol else 0,
        len(passutils.QWERTY_SYMB) if passinfo.qwertysymbol else 0,
    ]
    return sum(charsets) ** passinfo.length

def bruteforce_time(num_passwords, hashrate):
    return num_passwords/hashrate

def is_password_secure(pass_breaktime, passinfo):
    if 0 <= pass_breaktime <= LIMIT_TIMES[0]:
        passinfo.security = 0
    elif LIMIT_TIMES[0] < pass_breaktime <= LIMIT_TIMES[1]:
        passinfo.security = 1
    elif LIMIT_TIMES[1] < pass_breaktime <= LIMIT_TIMES[2]:
        passinfo.security = 2
    elif LIMIT_TIMES[2] < pass_breaktime <= LIMIT_TIMES[3]:
        passinfo.security = 3
    else:
        passinfo.security = 4

def set_color_message(passinfo_security):
    color_map = {0: "M", 1: "R", 2: "Y", 3: "C", 4: "G"}
    return color_map.get(passinfo_security, "RST")

def checkpass():
    try:
        password = get_password()
        passinfo = passutils.PasswordInfo()
        analyze_password(password, passinfo)

        if analyze_password_bruteforce(passinfo):
            num_passwords = calc_passwords(passinfo)
            pass_breaktime = bruteforce_time(num_passwords, DEFAULT_HASHCALC)
            breaktime_text = secs_to_time(pass_breaktime)
            is_password_secure(pass_breaktime, passinfo)
            breaktime_text_color = set_color_message(passinfo.security)

            print(f"Tiempo para romper la contraseña: ", end = ""); cprint(breaktime_text, breaktime_text_color)
            try:
                getpass("\nPresione ENTER para volver al menú principal.")
            except KeyboardInterrupt:
                signal_handler_exit()

    except KeyboardInterrupt:
        signal_handler_return()
