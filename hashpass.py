import hashlib
import bcrypt

from getpass import getpass

from modules import passutils
from modules.utils import show_header, cprint, handle_program_exit, handle_task_stop

def select_hash_algorithm():
    print("Seleccione alguna de las siguientes opciones de hasheo:")
    print("1) MD5")
    print("2) SHA-1")
    print("3) bcrypt")
    print("4) hashteo\n")

    option = input("Opción seleccionada: ")

    if option not in ["1", "2", "3", "4"]:
        getpass("\nOpción no válida, presione ENTER para continuar.")
        return None
    
    return option

def hashteo(password):
    print("acá va el código de hashteo")

def hash_password(password, option):
    if option == "1":
        return hashlib.md5(password.encode()).hexdigest()
    if option == "2":
        return hashlib.sha1(password.encode()).hexdigest()
    if option == "3":
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    if option == "4":
        hashteo(password)

def hashpass():
    try:
        password = None
        while password == None:
            show_header("=== OPCIÓN 3: HASHEAR CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            password = passutils.input_password()
        
        option = None
        while option == None:
            show_header("=== OPCIÓN 3: HASHEAR CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            option = select_hash_algorithm()

        password_hash = hash_password(password, option)

        print("\nEl hash para la contraseña ingresada es: ", end=""); cprint(password_hash, "G")

        try:
            getpass("\nPresione ENTER para volver al menú principal.")
        except KeyboardInterrupt:
            handle_program_exit()

    except KeyboardInterrupt:
        handle_task_stop()