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

def select_hash_algorithm():
    """
    Muestra las opciones de algoritmos de hashing disponibles y solicita al usuario
    seleccionar uno de ellos.

    Returns:
        None | str: Opción seleccionada por el usuario ("1", "2", "3" o "4"),
                    o None si la entrada no es válida.
    """
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

def hash_password(password, option):
    """
    Genera el hash de la contraseña utilizando el algoritmo seleccionado.

    Args:
        password (str): Contraseña a hashear.
        option (str): Opción seleccionada ("1", "2", "3" o "4").

    Returns:
        str | bytes: Hash generado. Devuelve bytes si se usa bcrypt.
    """
    if option == "1":
        return hashlib.md5(password.encode()).hexdigest()
    if option == "2":
        return hashlib.sha1(password.encode()).hexdigest()
    if option == "3":
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    if option == "4":
        return hashteo(password)

def hashpass():
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
