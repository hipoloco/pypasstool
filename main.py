def mostrar_menu():
    
    
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Analizar contraseña")
    print("2. Generar contraseña")
    print("3. Hashear contraseña")
    print("4. Salir")
    
    
    opcion= input("Seleccione una opción: ")
    return opcion



def ejecutar_menu():
    
    while True:
        opcion=mostrar_menu()
        
        if opcion== "1":
            contrasena=input("Ingrese la contraseña para analizar: ")
            resultado=analizador_contrasena(contrasena)
            print("\nResultado del análisis:")
            for clave, valor in resultado.items():
                if clave != "sugerencias":
                    print(f"- {clave.capitalize()}: {valor}")
            if resultado["sugerencias"]:
                print("Sugerencias para mejorar tu contraseña:")
                for sugerencia in resultado["sugerencias"]:
                    print(f"  * {sugerencia}")
            
            











import re
def analizador_contrasena(contrasena):
    """
    :param contrasena: str, contraseña a analizar.
    :return: dict, resultado del analisis.
    """
    
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
        
    return resultado
        
        
        
        
