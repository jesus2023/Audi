import os
from dotenv import load_dotenv
import cx_Oracle
from datetime import datetime, timedelta

# Declarar connection como una variable global
connection = None

# Apuntar a la instalación del cliente Oracle
cx_Oracle.init_oracle_client(lib_dir=r'C:/instantclient_21_13 x64')

# Especifica la ruta absoluta al directorio que contiene el archivo key.env
load_dotenv("C:/Users/RPA/Documents/Proyectos_Rocketbot/Bot Auditoria/Insumos/Auditoria_Python/conx_bd/R1_HCI.env")

# Accede a las variables con el prefijo DB_
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_SERVICE = os.environ.get('DB_SERVICE')

def conectar_base_datos():
    global connection
    try:
        
        # Crear la cadena de conexión
        dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, service_name=DB_SERVICE)
        
        # Intentar conectar
        connection = cx_Oracle.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn)

        # Si no hay excepción, la conexión fue exitosa
        print("Conexión exitosa")
        return True
        
    except cx_Oracle.Error as error:
        # Manejar la excepción en caso de error de conexión
        print(f"Error de conexión: {error}")
        return False

    finally:
        # Cerrar la conexión en el bloque finally para asegurar que siempre se cierre
        if 'connection' in locals():
            connection.close()

def consultar_base_datos(fecha_ayer_0, itera_codszonas):

    cursor = None

    # Intentar conectar a la base de datos
    if conectar_base_datos():
        
        try:
            # Crear un cursor
            cursor = connection.cursor()

            # Ejecutar la consulta SQL
            sql_query = f"select * from SALDOS_TESORERIA where fecha='{fecha_ayer_0}' and codigo_zona={itera_codszonas}"
            
            cursor.execute(sql_query)
            
            # Obtener los resultados y almacenarlos en una lista de listas
            datos_db = [list(row) for row in cursor.fetchall()]

            # Devolver True si la consulta fue exitosa
            return True, datos_db

        except cx_Oracle.Error as error:
            # Manejar la excepción en caso de error en la consulta
            print(f"Error de consulta: {error}")
            return False, None

        finally:
            # Cerrar el cursor en el bloque finally para asegurar que siempre se cierre
            cursor.close()    
def consultar_base_datos_2(fecha_ayer_0, itera_cods_mont):

    cursor = None

    # Intentar conectar a la base de datos
    if conectar_base_datos():
        
        try:
            # Crear un cursor
            cursor = connection.cursor()

            # Ejecutar la consulta SQL
            sql_query = f"select * from SALDOS_TESORERIA where fecha='{fecha_ayer_0}' and codigo_zona='1077' and CENTRO_COSTO='{itera_cods_mont}'"
            cursor.execute(sql_query)
            
            # Obtener los resultados y almacenarlos en una lista de listas
            datos_db_2 = [list(row) for row in cursor.fetchall()]

            # Devolver True si la consulta fue exitosa
            return True, datos_db_2

        except cx_Oracle.Error as error:
            # Manejar la excepción en caso de error en la consulta
            print(f"Error de consulta: {error}")
            return False, None

        finally:
            # Cerrar el cursor en el bloque finally para asegurar que siempre se cierre
            cursor.close()