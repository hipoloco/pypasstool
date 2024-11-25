from getpass import getpass

from modules import passutils
from modules.utils import clear_screen, cprint, secs_to_time
from modules.constants import DEFAULT_HASHCALC, COLOR_LIMIT_TIMES

passinfo = {
    "length": 0,
    "number": False,
    "lowercase": False,
    "uppercase": False,
    "secsymbol": False,
    "commsymbol": False,
    "qwertysymbol": False,
    "security": 0
}

def header():
    clear_screen()
    cprint("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS ===\n", "Y")

def get_password():
    while True:
        header()
        password = getpass("Ingrese la contraseña a analizar: ")

        if not password:
            getpass("\nNo ha ingresado una contraseña, presione ENTER para continuar.")
            continue
        if " " in password:
            getpass("\nLa contraseña no puede tener espacios, presione ENTER para continuar.")
            continue
        if not passutils.validate_password(password):
            getpass("\nLa contraseña contiene caracteres inválidos, presione ENTER para continuar.")
            continue

        repeat_pass = getpass("Ingrese nuevamente la contraseña: ")
        if password != repeat_pass:
            getpass("\nLas contraseñas no coinciden, presione ENTER para continuar.")
            continue

        return password

def analyze_password(password):
    passinfo["length"] = len(password)
    passinfo["number"] = passutils.pass_has_chartype(password, passutils.NUMS)
    passinfo["lowercase"] = passutils.pass_has_chartype(password, passutils.LOWER)
    passinfo["uppercase"] = passutils.pass_has_chartype(password, passutils.UPPER)
    passinfo["secsymbol"] = passutils.pass_has_chartype(password, passutils.SEC_SYMB)
    passinfo["commsymbol"] = passutils.pass_has_chartype(password, passutils.COMM_SYMB)
    passinfo["qwertysymbol"] = passutils.pass_has_chartype(password, passutils.QWERTY_SYMB)

    while True:
        header()
        print("Resumen de la contraseña ingresada:")
        cprint("[*] ", "Y", ""); print("Longitud: ", end=""); cprint(str(passinfo["length"]), "R") if passinfo["length"] <= 10 else cprint(str(passinfo["length"]), "G")
        cprint("[*] ", "Y", ""); print("Tiene números: ", end=""); cprint("Si", "G") if passinfo["number"] else cprint("No", "R")
        cprint("[*] ", "Y", ""); print("Tiene letras minúsculas: ", end=""); cprint("Si", "G") if passinfo["lowercase"] else cprint("No", "R")
        cprint("[*] ", "Y", ""); print("Tiene letras mayúsculas: ", end=""); cprint("Si", "G") if passinfo["uppercase"] else cprint("No", "R")
        cprint("[*] ", "Y", ""); print("Tiene símbolos: ", end="")
        if passinfo["secsymbol"] or passinfo["commsymbol"] or passinfo["qwertysymbol"]:
            cprint("Si", "G")
            cprint("[*] ", "Y", ""); print("Compatibilidad de símbolos utilzados: ", end="")
            if passinfo["qwertysymbol"]:
                cprint("Baja", "R")
            elif passinfo["commsymbol"]:
                cprint("Media", "C")
            else:
                cprint("Alta", "G")
        else:
            cprint("No", "R")

        confirmation = input("\nDesea verificar la seguridad de su contraseña? [S/n]: ")
        if confirmation not in ["", "s", "S", "n", "N"]:
            getpass("\nOpción incorrecta, presione ENTER para continuar.")
            continue
        if confirmation in ["n", "N"]:
            getpass("\nVerificación cancelada, presione ENTER para volver al menú principal.")
            return False
        
        return True

def calc_passwords(pass_lenght):
    charset = 0
    if passinfo["number"]:
        charset += len(passutils.NUMS)
    if passinfo["lowercase"]:
        charset += len(passutils.LOWER)
    if passinfo["uppercase"]:
        charset += len(passutils.UPPER)
    if passinfo["secsymbol"]:
        charset += len(passutils.SEC_SYMB)
    if passinfo["commsymbol"]:
        charset += len(passutils.COMM_SYMB)
    if passinfo["qwertysymbol"]:
        charset += len(passutils.QWERTY_SYMB)

    return charset**pass_lenght

def bruteforce_time(num_passwords, hashrate):
    return num_passwords/hashrate

def is_password_secure(pass_breaktime):
    if 0 <= pass_breaktime <= COLOR_LIMIT_TIMES[0]:
        passinfo["security"] = 0
    elif COLOR_LIMIT_TIMES[0] < pass_breaktime <= COLOR_LIMIT_TIMES[1]:
        passinfo["security"] = 1
    elif COLOR_LIMIT_TIMES[1] < pass_breaktime <= COLOR_LIMIT_TIMES[2]:
        passinfo["security"] = 2
    elif COLOR_LIMIT_TIMES[2] < pass_breaktime <= COLOR_LIMIT_TIMES[3]:
        passinfo["security"] = 3
    else:
        passinfo["security"] = 4

def set_color_message():
    if passinfo["security"] == 0:
        return "M"
    if passinfo["security"] == 1:
        return "R"
    if passinfo["security"] == 2:
        return "Y"
    if passinfo["security"] == 3:
        return "C"
    if passinfo["security"] == 4:
        return "G"
    else:
        return "RST"

def checkpass():
    password = get_password()

    if analyze_password(password):
        num_passwords = calc_passwords(passinfo["length"])
        pass_breaktime = bruteforce_time(num_passwords, DEFAULT_HASHCALC)
        breaktime_text = secs_to_time(pass_breaktime)
        is_password_secure(pass_breaktime)
        breaktime_text_color = set_color_message()

        print(f"Tiempo para romper la contraseña: ", end = ""); cprint(breaktime_text, breaktime_text_color)
        getpass("\nPresione ENTER para volver al menú principal.")