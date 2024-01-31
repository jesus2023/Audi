import os

def log_successful():
    # Ruta específica donde deseas guardar el archivo
    ruta_especifica = "C:/Users/Deimer Yepes/Documents/Pruebas/"

    # Nombre del archivo
    nombre_archivo = "Ejecución_Auditoría_BD.txt"

    # Ruta completa del archivo
    ruta_completa = os.path.join(ruta_especifica, nombre_archivo)

    # Contenido del archivo
    contenido_archivo = "True"

    # Crear el archivo en la ruta especificada
    with open(ruta_completa, "w") as file:
        file.write(contenido_archivo)

    print(f"Archivo guardado en: {ruta_completa}")

def log_fail():
    # Ruta específica donde deseas guardar el archivo
    ruta_especifica = "C:/Users/Deimer Yepes/Documents/Pruebas/"

    # Nombre del archivo
    nombre_archivo = "Ejecución_Auditoría_BD.txt"

    # Ruta completa del archivo
    ruta_completa = os.path.join(ruta_especifica, nombre_archivo)

    # Contenido del archivo
    contenido_archivo = "False"

    # Crear el archivo en la ruta especificada
    with open(ruta_completa, "w") as file:
        file.write(contenido_archivo)

    print(f"Archivo guardado en: {ruta_completa}")
