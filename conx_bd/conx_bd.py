import os
from dotenv import load_dotenv
import cx_Oracle

# Cargar variables de entorno desde el archivo .env
load_dotenv("C:/Users/RPA/Desktop/conx_bd/gamble.env")

# Acceder a las variables de entorno
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_service = os.environ.get("DB_SERVICE")

# Crear la cadena de conexión
dsn = cx_Oracle.makedsn(db_host, db_port, service_name=db_service)
connection = cx_Oracle.connect(user=db_user, password=db_password, dsn=dsn)

# Crear un cursor
cursor = connection.cursor()

# Ejecutar la consulta SQL

sql_query = "SELECT PRS_DOCUMENTO, PORCBEPS FROM CONTRATOSVENTA WHERE FECHAFINAL IS NULL AND PRS_DOCUMENTO IN (1069490257, 1065001847, 1067908542)"

cursor.execute(sql_query)

# Obtener los resultados
for row in cursor.fetchall():
    print(row)

# Cerrar la conexión cuando hayas terminado
connection.close()


# CONEXIÓN CON BD MYSQL

# import os
# from dotenv import load_dotenv
# import mysql.connector

# # Cargar variables de entorno desde el archivo .env
# load_dotenv("C:/Users/RPA/Desktop/conx_bd/gamble.env")

# # Acceder a las variables de entorno
# db_host = os.environ.get("DB_HOST")
# db_port = os.environ.get("DB_PORT")
# db_user = os.environ.get("DB_USER")
# db_password = os.environ.get("DB_PASSWORD")
# db_database = os.environ.get("DB_DATABASE")

# # Crear la conexión a la base de datos MySQL
# connection = mysql.connector.connect(
#     host=db_host,
#     port=db_port,
#     user=db_user,
#     password=db_password,
#     database=db_database
# )

# # Crear un cursor
# cursor = connection.cursor()

# # Ejecutar la consulta SQL
# sql_query = "SELECT PRS_DOCUMENTO, PORCBEPS FROM CONTRATOSVENTA WHERE FECHAFINAL IS NULL AND PRS_DOCUMENTO IN (1069490257, 1065001847, 1067908542)"
# cursor.execute(sql_query)

# # Obtener los resultados
# for row in cursor.fetchall():
#     print(row)

# # Cerrar el cursor
# cursor.close()

# # Cerrar la conexión cuando hayas terminado
# connection.close()

[('1065001847, 3', '1067908542, 3', '1069490257, 3')], [('1065001847, 3', '1067908542, 3', '1069490257, 3')]

