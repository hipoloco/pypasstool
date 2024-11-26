import os
import random
import string
import hashlib

def generar_contraseña(longitud=12, incluir_mayusculas=True, incluir_numeros=True, incluir_simbolos=True):
    """
    Genera una contraseña segura basada en las opciones proporcionadas.

    :param longitud: Longitud de la contraseña (por defecto 12 caracteres).
    :param incluir_mayusculas: Incluir letras mayúsculas (True por defecto).
    :param incluir_numeros: Incluir números (True por defecto).
    :param incluir_simbolos: Incluir símbolos (True por defecto).
    :return: Contraseña generada.
    """
    caracteres = string.ascii_lowercase  # Letras minúsculas
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation

    if not caracteres:
        raise ValueError("Debe incluir al menos un tipo de carácter.")

    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

def hash_contraseña(contraseña):
    """
    Aplica un hash seguro a una contraseña.
    
    :param contraseña: Contraseña original.
    :return: Contraseña en formato hash (SHA-256).
    """
    return hashlib.sha256(contraseña.encode()).hexdigest()

def menu():
    """
    Menú interactivo para generar y hashear contraseñas.
    """
    while True:
        print("\n=== Generador de Contraseñas ===")
        print("1. Generar contraseña")
        print("2. Hash de contraseña")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            try:
                longitud = int(input("Longitud de la contraseña (número entero): "))
                incluir_mayusculas = input("¿Incluir mayúsculas? (s/n): ").lower() == 's'
                incluir_numeros = input("¿Incluir números? (s/n): ").lower() == 's'
                incluir_simbolos = input("¿Incluir símbolos? (s/n): ").lower() == 's'
                
                contraseña = generar_contraseña(longitud, incluir_mayusculas, incluir_numeros, incluir_simbolos)
                print(f"Contraseña generada: {contraseña}")
            except ValueError as e:
                print(f"Error: {e}")
        elif opcion == '2':
            contraseña = input("Ingrese la contraseña a hashear: ")
            print(f"Hash (SHA-256): {hash_contraseña(contraseña)}")
        elif opcion == '3':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()

def hashpass():
    try:
        password = None
        while password == None:
            show_header()
            password = passutils.input_password()
        
        passinfo = passutils.PasswordInfo()
        analyze_password_props(password, passinfo)

        if confirm_bruteforce_analysis(passinfo):
            num_passwords = calc_password_combinations(passinfo)
            pass_breaktime = get_bruteforce_time(num_passwords, DEFAULT_DEVICE_HASHRATE)
            breaktime_text = format_time(pass_breaktime)
            set_password_secururity(pass_breaktime, passinfo)
            breaktime_text_color = get_security_color(passinfo.security)
            improvements_list = password_improvements(passinfo)

            show_bruteforce_summary(improvements_list, breaktime_text, breaktime_text_color)
            try:
                getpass("\nPresione ENTER para volver al menú principal.")
            except KeyboardInterrupt:
                handle_program_exit()

    except KeyboardInterrupt:
        handle_task_stop()