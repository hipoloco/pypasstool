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
    # Convertir la entrada a bytes
    pass_byte_array = password[::-1].encode('utf-8')

    # Inicializar un array de 256 bits (32 bytes)
    hash_array = [0] * 32

    # Procesar cada byte
    for i, byte in enumerate(pass_byte_array):
        # Mezclar el byte en todas las posiciones del array
        for j in range(32):
            hash_array[j] ^= (byte + i + j) & 0xFF
            hash_array[j] = ((hash_array[j] << 1) | (hash_array[j] >> 1)) & 0xFF  # Rotar bits

    # Convertir el array a un string hexadecimal
    return ''.join(f'{x:02x}' for x in hash_array)

def hash_password(password, option):
    if option == "1":
        return hashlib.md5(password.encode()).hexdigest()
    if option == "2":
        return hashlib.sha1(password.encode()).hexdigest()
    if option == "3":
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    if option == "4":
        return hashteo(password)

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

# Bloque para prevenir la ejecución directa del módulo.
if __name__ == "__main__":
    cprint("\n[*] Este módulo no puede ser ejecutado directamente.\n", "R")