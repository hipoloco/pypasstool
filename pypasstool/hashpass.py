"""
hashpass.py

Este módulo permite generar un hash para una contraseña ingresada por el usuario utilizando
algoritmos de hashing estándar (MD5, SHA-1, bcrypt) o un algoritmo de hash personalizado.
"""

import hashlib
import bcrypt

from getpass import getpass

from utils import passutils
from utils.utils import show_header, cprint, handle_program_exit, handle_task_stop
from models.hashpass import find_password_id, get_hash_algo, find_password_hash, insert_password_hash
from models.common import insert_password

def select_hash_algorithm(db_conn):
    """
    Muestra un menú para seleccionar un algoritmo de hashing.

    Args:
        db_conn: Conexión a la base de datos.

    Returns:
        dict | None: Un diccionario con el ID del algoritmo y su nombre si se selecciona
            una opción válida, None si la opción es inválida.
    """
    hash_algo = get_hash_algo(db_conn)
    
    print("Seleccione alguna de las siguientes opciones de hasheo:")
    for opt, (id_algo, algo_name) in enumerate(hash_algo, 1):
        print(f"{opt}. {algo_name}")

    option = input("\nOpción seleccionada: ")
    if option.isdigit() and 1 <= int(option) <= len(hash_algo):
        id_algo, algo_name = hash_algo[int(option) - 1]
        return {"id_algo": id_algo, "algo_name": algo_name}
    else:
        getpass("\nOpción ino válida, presione ENTER para continuar.")
        return None

def hashteo(password):
    """
    Genera un hash utilizando un algoritmo de hashing personalizado.

    Este algoritmo realiza las siguientes operaciones:
    - Convierte la contraseña a un array de bytes.
    - Inicializa un array de 256 bits (32 bytes) con valores en cero.
    - Procesa cada byte de la contraseña invirtiendo su orden y lo mezcla en todas
      las posiciones del array utilizando operaciones XOR y rotaciones de bits.

    Args:
        password (str): Contraseña a hashear.

    Returns:
        str: Representación en hexadecimal del hash generado.
    """
    # Convertir la contraseña a un array de bytes invirtiendo su orden
    # Esto añade un primer nivel de transformación simple al input.
    pass_byte_array = password[::-1].encode('utf-8')

    # Inicializar un array de 32 bytes (256 bits) con ceros.
    # Este array actúa como el estado interno del hash.
    hash_array = [0] * 32

    # Procesar cada byte del array generado a partir de la contraseña.
    for i, byte in enumerate(pass_byte_array):
        # Mezclar el byte actual en todas las posiciones del array hash.
        for j in range(32):
            # Operación XOR entre el byte actual y un valor derivado de su índice y el índice del array hash.
            # Esto introduce aleatoriedad en función de la posición del byte y la posición del array hash.
            hash_array[j] ^= (byte + i + j) & 0xFF
            
            # Rotar los bits hacia la izquierda y luego hacia la derecha para redistribuir los valores.
            # La operación asegura que los bits menos significativos se mezclen en todo el array.
            hash_array[j] = ((hash_array[j] << 1) | (hash_array[j] >> 1)) & 0xFF

    # Convertir el array final a una representación en formato hexadecimal.
    # Cada valor del array (0-255) se transforma en un string de dos dígitos hexadecimales.
    return ''.join(f'{x:02x}' for x in hash_array)

def hash_password(password, hash):
    """
    Hashea una contraseña utilizando el algoritmo especificado.

    Args:
        password (str): Contraseña a hashear.
        hash (str): Algoritmo de hashing a utilizar.

    Returns:
        str | None: El hash de la contraseña si el algoritmo es válido,
            None en caso de no soportar el algoritmo.
    """
    if hash == "MD5":
        return hashlib.md5(password.encode()).hexdigest()
    elif hash == "SHA-1":
        return hashlib.sha1(password.encode()).hexdigest()
    elif hash == "BCRYPT":
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    elif hash == "HASHTEO":
        return hashteo(password)
    else:
        return None

def handle_password_hash(db_conn, pwd_id, hash, password):
    """
    Maneja el proceso de inserción del hash de la contraseña en la base de datos.
    Verifica si el algoritmo de hash es soportado, genera el hash y lo inserta en la base de datos.

    Args:
        db_conn: Conexión a la base de datos.
        pwd_id: ID de la contraseña.
        hash: Diccionario con información del algoritmo de hash.
        password: Contraseña ingresada por el usuario.

    Returns:
        str | None: El hash generado si el algoritmo es soportado, None en caso contrario.
    """
    password_hash = hash_password(password, hash["algo_name"])
    if password_hash:
        insert_password_hash(db_conn, pwd_id, hash["id_algo"], password_hash)
        return password_hash
    else:
        return None

def hashpass(db_conn):
    """
    Punto de entrada principal para la funcionalidad de hasheo de contraseñas.

    Solicita una contraseña al usuario, permite seleccionar un algoritmo de hashing,
    genera el hash correspondiente y lo muestra en pantalla.

    Maneja interrupciones (Ctrl+C) y permite salir del programa de manera controlada.
    """
    try:
        password = None
        while password == None:
            show_header("=== OPCIÓN 3: HASHEAR CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            password = passutils.input_password()
        
        hash = None
        while hash == None:
            show_header("=== OPCIÓN 3: HASHEAR CONTRASEÑAS (CTRL+C PARA VOLVER) ===\n")
            hash = select_hash_algorithm(db_conn)
        
        hashedpwd = passutils.hash_password(password)
        pwd_id = find_password_id(db_conn, hashedpwd)
        if not pwd_id:
            pwd_id = insert_password(db_conn, hashedpwd)
            password_hash = handle_password_hash(db_conn, pwd_id, hash, password)
        else:
            password_hash = find_password_hash(db_conn, pwd_id, hash["id_algo"])
            if not password_hash:
                password_hash = handle_password_hash(db_conn, pwd_id, hash, password)
        
        if not password_hash:
            cprint("\n[!] El algoritmo de hash seleccionado no es soportado.", "R")
        else:
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
