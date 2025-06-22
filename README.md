
# pypasstool: gestor de contraseñas

Este proyecto es una herramienta interactiva para analizar, generar y hashear contraseñas, diseñada para proporcionar una experiencia segura y completa en la gestión de contraseñas.

**URL del proyecto:** [https://github.com/hipoloco/pypasstool](https://github.com/hipoloco/pypasstool)

## Novedades: Uso de base de datos

A partir de la versión 2.0.0, **pypasstool** utiliza una base de datos SQLite para almacenar información relevante sobre dispositivos, algoritmos de hash, propiedades de contraseñas y resultados de análisis de fuerza bruta. Esto permite:

- Consultar y reutilizar resultados de análisis previos.
- Registrar y gestionar dispositivos y algoritmos de hash disponibles.
- Mejorar la eficiencia y trazabilidad de los análisis realizados.

## Funcionalidades

1. **Analizador de Contraseñas**: Permite evaluar la seguridad de una contraseña basada en:
   - Propiedades de la contraseña (longitud, tipos de caracteres).
   - Tiempo estimado para romper la contraseña mediante ataques de fuerza bruta.
   - Nivel de seguridad y sugerencias para mejorarla.
   - Almacenamiento de resultados en la base de datos.
   - **Evita evaluaciones duplicadas:** Antes de realizar un nuevo análisis de fuerza bruta para una contraseña con las mismas características, consulta la base de datos y reutiliza el resultado si ya existe, optimizando así el rendimiento y evitando cálculos innecesarios.

2. **Generador de Contraseñas**: Genera contraseñas seguras según los criterios del usuario:
   - Longitud personalizada (12-30 caracteres).
   - Inclusión de números, letras (mayúsculas y minúsculas) y símbolos.
   - Nivel de compatibilidad de los símbolos.
   - Almacenamiento de las contraseñas generadas de forma segura en la base de datos.
   - **Evita la generación de contraseñas duplicadas:** Antes de otrogar una nueva contraseña, se consulta la base de datos para asegurarse de que no exista una igual, garantizando así la unicidad de las contraseñas generadas.

3. **Hashing de Contraseñas**: Proporciona la opción de generar hashes de contraseñas utilizando:
   - Algoritmos estándar (MD5, SHA-1, bcrypt).
   - Algoritmo personalizado (`hashteo`).
   - Almacenamiento de los hashes calculados en la base de datos.
   - **Evita el cálculo de hashes duplicados:** Antes de calcular y almacenar un hash para una contraseña y algoritmo determinados, se consulta la base de datos para evitar duplicados y reutilizar resultados ya existentes.

## Requisitos Previos

- Python 3.7 o superior.
- `pip` instalado para la gestión de dependencias.

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/hipoloco/pypasstool
   cd pypasstool
   ```

2. Instalar las dependencias:
   - En Linux/MacOS:
     ```bash
     bash ./install_dependencies.sh
     ```
   - En Windows:
     ```cmd
     install_dependencies.bat
     ```

## Uso

Ejecuta el archivo `pypasstool/main.py` para iniciar la aplicación. Se mostrará un menú interactivo con las siguientes opciones:

1. **Analizar Contraseña**:
   - Evalúa la seguridad de una contraseña ingresada.
   - Permite seleccionar el dispositivo y algoritmo de hash desde la base de datos.
   - Consulta y almacena los resultados del análisis en la base de datos.
2. **Generar Contraseña**:
   - Crea una contraseña según los criterios seleccionados por el usuario.
3. **Hashear Contraseña**:
   - Genera un hash de una contraseña utilizando el algoritmo elegido.
4. **Salir**:
   - Finaliza la aplicación.

Ejemplo de ejecución en Linux/MacOS:
```bash
python pypasstool/main.py
```

Ejemplo de ejecución en Windows:
```cmd
python pypasstool\main.py
```

## Archivos y Estructura

### Principales Archivos
- **`pypasstool/main.py`**: Punto de entrada principal que controla el flujo de la aplicación.
- **`pypasstool/checkpass.py`**: Módulo para analizar la seguridad de contraseñas.
- **`pypasstool/passgenerator.py`**: Módulo para generar contraseñas seguras.
- **`pypasstool/hashpass.py`**: Módulo para hashear contraseñas.
- **`pypastool/models/init_db.py y seed_db.py`: Scripts para inicializar y poblar la base de datos.

### Scripts de Instalación
- **`install_dependencies.sh`** (Linux/MacOS): Script para instalar las dependencias desde `requirements.txt`.
- **`install_dependencies.bat`** (Windows): Script equivalente para sistemas Windows.

### Dependencias
Listado en `requirements.txt`:
- `bcrypt`: Biblioteca para trabajar con hashing seguro.
- Versión personalizada de `pwinput`:
  ```plaintext
  git+https://github.com/binbash23/pwinput.git
  ```

## Colaboradores

- **hipoloco**: [https://github.com/hipoloco](https://github.com/hipoloco)
- **Kabuta14**: [https://github.com/Kabua14](https://github.com/Kabua14)
- **CasTeo7**: [https://github.com/CasTeo7](https://github.com/CasTeo7)

## Nota

Este proyecto fue realizado como obligatorio de la materia "Introducción a la programación" del primer semestre del Tecnólogo en Ciberseguridad de CETP-UTU y adaptado a la exigencias del obligatorio de la materia "Introducción a las bases de datos" del segundo semestre de la mencionada carrera.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos para colaborar:

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad o corrección (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commits claros y descriptivos.
4. Envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.
