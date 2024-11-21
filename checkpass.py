from getpass import getpass

from modules import passutils
from modules.utils import clear_screen, cprint

passinfo = {
    "length": 0,
    "number": False,
    "lowercase": False,
    "uppercase": False,
    "secsymbol": False,
    "commsymbol": False,
    "qwertysymbol": False,
}

def get_password():
    while True:
        clear_screen()
        cprint("=== OPCIÓN 1: ANALIZADOR DE CONTRASEÑAS ===\n", "Y")
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

def calc_passwords():
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

    return charset ** passinfo["length"]

"""         contrasena=input("Ingrese la contraseña para analizar: ")
            resultado=analizador_contrasena(contrasena)
            print("\nResultado del análisis:")
            for clave, valor in resultado.items():
                if clave != "sugerencias":
                    print(f"- {clave.capitalize()}: {valor}")
            if resultado["sugerencias"]:
                print("Sugerencias para mejorar tu contraseña:")
                for sugerencia in resultado["sugerencias"]:
                    print(f"  * {sugerencia}") """

""" import re
def analizador_contrasena(contrasena):
    ""
    :param contrasena: str, contraseña a analizar.
    :return: dict, resultado del analisis.
    ""
    
    resultado={
        "longitud": False,
        "mayusculas": False,
        "minusculas": False,
        "numeros": False,
        "caracteres_especiales": False,
        "sin_patrones_comunes": True,
        "fortaleza": "debil",
        "sugerencias": []
    }
    
    
    if len(contrasena) >=8:
        resultado["longitud"]=True
    else:
        resultado["sugerencias"].append ("Usa al menos 8 caracteres")
        
    
    if any(c.isupper() for c in contrasena):
        resultado["mayusculas"] = True
    else:
        resultado["sugerencias"].append ("Incluye al menos una letra mayúscula")
    
    if any (c.islower() for c in contrasena):
        resultado["minusculas"]=True
    else:
        resultado["sugerencias"].append ("Incluye al menos una letra minúscula")
        
    if any(c.isdigit() for c in contrasena):
        resultado["numeros"]=True
    else:
        resultado["sugerencias"].append ("Incluye al menos un número")
        
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', contrasena):
        resultado["caracteres_especiales"]=True
    else:
        resultado["sugerencias"].append ("Incluye al menos un carácter especial (!, @, #, etc.).")
    
    patrones_comunes= [r"(.)\1{2,}", r"1234", r"abcd", r"password", r"qwerty"]
    for patron in patrones_comunes:
        if re.search(patron, contrasena, re.INGNORECASE):
             resultado["sin_patrones_comunes"]=False
             resultado["sugerencias"].append ("Evite patrones comunes como '1234', 'abcd', o repeticiones consecutivas.")
             break
         
    
    if all ([
        resultado["longitud"],
        resultado["mayusculas"],
        resultado["minusculas"],
        resultado["numeros"],
        resultado["caracteres_especiales"],
        resultado["sin_patrones_comunes"],
    ]):
        resultado["fortaleza"]= "Fuerte"
        
    elif len(resultado["sugerencias"]) <=2:
        resultado["fortaleza"]="Moderada"
        
    return resultado """