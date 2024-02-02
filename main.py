import shutil
from datetime import datetime, timedelta
import os
from config import conectar_base_datos, consultar_base_datos, consultar_base_datos_2
from excel_functions import generar_archivo_excel, generar_archivo_excel_2
from Correo_soporte import enviar_soporte
from Correo_soporte2 import enviar_soporte2
from Correo_cliente import enviar_cliente
from Copy_files import copy_files
from Gmail import correo_exitoso
from logs import log_successful, log_fail

# Inicializar variables
cont_nombre = 0 
cod_zonas = ['1692', '1708', '1409', '1390', '1431', '1696', '1703']
nom_zonas = ['MONTELIBANO', 'TIERRA-ALTA', 'AYAPEL', 'PLANETA-RICA', 'CERETE', 'LORICA', 'SAHAGUN']
path_arch_audi1 = 'C:/Users/RPA/Documents/Proyectos_Rocketbot/Bot Auditoria/Insumos/Archivos/Auditoria'# Cambiar antes de probar!!!!!
cod_zonas_mont = ['MOCARI - ZONA URBANA MONTERIA', 'PRADERA - ZONA URBANA MONTERIA', 'MOGAMBO - ZONA URBANA MONTERIA', 'GRANJA - ZONA URBANA MONTERIA','DORADO - ZONA URBANA MONTERIA','OFIC.PRINCIPAL MONTERIA - ZONA URBANA MONTERIA', 'PUERTO ESCONDIDO - ZONA URBANA MONTERIA', 'SANTA LUCIA - ZONA URBANA MONTERIA', 'SAN ANTERITO - ZONA URBANA MONTERIA', 'CANALETE - ZONA URBANA MONTERIA', 'CARRISAL - ZONA URBANA MONTERIA', 'LOS CORDOBAS - ZONA URBANA MONTERIA']
noms_zonas_mont = ['MOCARI', 'PRADERA', 'MOGAMBO', 'GRANJA','DORADO', 'OFIC.PRINCIPAL MONTERIA', 'PUERTO ESCONDIDO', 'SANTA LUCIA', 'SAN ANTERITO', 'CANALETE', 'CARRISAL', 'LOS CORDOBAS']

# Especifica la ruta de la carpeta que deseas eliminar y crear
carpeta_a_eliminar_y_crear = 'C:/Users/RPA/Documents/Proyectos_Rocketbot/Bot Auditoria/Insumos/Email'

# Intenta eliminar la carpeta y su contenido
try:
    shutil.rmtree(carpeta_a_eliminar_y_crear)
    print(f'Carpeta {carpeta_a_eliminar_y_crear} eliminada con éxito.')
except OSError as e:
    print(f'Error al eliminar la carpeta: {e}')

# Obtén las fechas
fecha_log = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
fecha_ayer_0 = (datetime.now() - timedelta(hours=24)).strftime("%d/%b/%Y")
fecha_ayer_1 = (datetime.now() - timedelta(hours=24)).strftime("%d-%m-%Y")
dia = (datetime.now() - timedelta(hours=24)).strftime("%d")
mes = [datetime.now()-timedelta(hours=24)][0].strftime("%b")
anio = [datetime.now()-timedelta(hours=24)][0].strftime("%Y")

# Verifica la conexión a la base de datos del archivo config.py
valida_conn_bd = conectar_base_datos()

if valida_conn_bd:
    # Intenta crear la carpeta
    try:
        os.makedirs(carpeta_a_eliminar_y_crear)
        print(f'Carpeta {carpeta_a_eliminar_y_crear} creada con éxito.')
    except OSError as e:
        print(f'Error al crear la carpeta: {e}')

    for itera_nomzona in cod_zonas:

        # itera los nombres de las zonas
        itera_nomzona = nom_zonas[cont_nombre]

        # Verifica la consulta a la base de datos del archivo config.py
        valida_datos_bd, datos_db = consultar_base_datos()

        if valida_datos_bd:
            
            # Llamada a la función que crea el archivo Excel y se le pasa la variable datos_db del archivo excel_functions.py
            generar_archivo_excel(datos_db, fecha_ayer_1, itera_nomzona, path_arch_audi1)

            # Resetear variables al final del código
            datos_bd = None
            itera_nomzona = None
            abre_audi = None
            num_filas = None
            guarda_arch = None
            guarda_arch_email = None
            valida_datos_bd = None

            # Incremento de la variable
            cont_nombre = cont_nombre + 1
        else:
            # Llamada a la función de enviar_soporte desde Correo_soporte.py
            enviar_soporte()

            # Llamada a la función de enviar_cliente desde Correo_cliente.py
            enviar_cliente()
else:
    # Llamada a la función de enviar_soporte desde Correo_soporte2.py    
    enviar_soporte2()

    # Llamada a la función de enviar_cliente desde Correo_cliente.py
    enviar_cliente()

# Reseteo el contador para volver a usarlo
cont_nombre = 0

for itera_cods_mont in cod_zonas_mont:

    # itera los nombres de las zonas
    itera_nom_mont = noms_zonas_mont[cont_nombre]

    # Verifica la consulta a la base de datos del archivo config.py
    valida_datos_bd2, datos_db_2 = consultar_base_datos_2(fecha_ayer_0, itera_cods_mont)    

    if valida_datos_bd2:

        # Llamada a la función que crea el archivo Excel y se le pasa la variable datos_db_2 del archivo excel_functions.py
        generar_archivo_excel_2(datos_db_2, fecha_ayer_1, itera_nom_mont, path_arch_audi1)

        # Resetear variables al final del código
        datos_bd2 = None
        itera_nom_mont = None
        abre_audi = None
        num_filas = None
        guarda_arch = None
        guarda_arch_email = None
        valida_datos_bd2 = None
        itera_cods_mont = None
        itera_nom_mont = None

        # Incremento de la variable
        cont_nombre = cont_nombre + 1

    else:

        # Llamada a la función de enviar_soporte desde Correo_soporte.py
        enviar_soporte()

        # Llamada a la función de enviar_cliente desde Correo_cliente.py
        enviar_cliente()

# Copiar archivos a Drive
copy_files()

try:
    correo_exitoso()
    log_successful()

except Exception as e:
    log_fail()
