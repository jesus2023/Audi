import os
import shutil

def copy_files():
    # Rutas de las carpetas origen y destino
    carpeta_origen = 'C:/Users/RPA/Desktop/Audi/Email' # C:/Users/RPA/Documents/Proyectos_Rocketbot/Bot Auditoria/Insumos/Email
    carpeta_destino = 'C:/Users/RPA/Desktop/Audi/Archivos auditoria' # G:/Mi unidad/Archivos auditoria

    # Lista de archivos en la carpeta de origen
    archivos = os.listdir(carpeta_origen)

    # Iterar sobre los archivos y copiarlos a la carpeta de destino
    for archivo in archivos:
        ruta_origen = os.path.join(carpeta_origen, archivo)
        ruta_destino = os.path.join(carpeta_destino, archivo)
        shutil.copy2(ruta_origen, ruta_destino)  # Puedes usar shutil.copy en lugar de shutil.copy2 si no necesitas preservar los metadatos

