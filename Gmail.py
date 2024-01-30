import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

#Sin embargo, Google no permitirá el inicio de sesión a través de smtplib 
#porque ha marcado este tipo de inicio de sesión como "menos seguro".
#Para solucionar este problema, vaya a https://www.google.com/settings/security/lesssecureapps
#mientras está conectado a su cuenta de Google y a "Permitir aplicaciones menos seguras".

# Configuración del mensaje y credenciales
sender_email = "jesus.suarez@record.com.co"
password = "mamona2023"

# Lista de destinatarios
recipient_emails = ["jesus.suarez@record.com.co", "anderson.diaz@record.com.co"]

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ", ".join(recipient_emails)  # Concatena las direcciones de correo con comas
msg['Subject'] = "Archivos adjuntos"

message = "Adjunto encontrarás los archivos de la carpeta."

msg.attach(MIMEText(message, 'plain'))

# Carpeta que contiene los archivos que deseas adjuntar
carpeta_con_archivos = "C:/Users/Deimer Yepes/Documents/Documentos de prueba" #Cambiar la ruta por la solicitada

# Obtener la lista de archivos en la carpeta
archivos_en_carpeta = os.listdir(carpeta_con_archivos)

# Adjuntar cada archivo al mensaje
for archivo in archivos_en_carpeta:
    archivo_path = os.path.join(carpeta_con_archivos, archivo)
    with open(archivo_path, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(archivo))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(archivo)}"'
        msg.attach(part)

# Crear el servidor y enviar el mensaje
with smtplib.SMTP('smtp.gmail.com:587') as server:
    server.starttls()

    try:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())
        print(f"Correo electrónico con archivos adjuntos enviado exitosamente a {recipient_emails}")
    except Exception as e:
        print(f"Error: {e}")
