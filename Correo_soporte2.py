import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

def enviar_soporte2():
    # Configuración del mensaje y credenciales
    sender_email = "user" # Cambiar las credenciales
    password = "password" 

    # Lista de destinatarios
    recipient_emails = ["jesus.suarez@record.com.co", "anderson.diaz@record.com.co"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = "Error en la ejecución del Bot Auditoria BD, log generado."

    message = "Ha ocurrido un error con en la ejecución del Bot Auditoría BD, por favor valide el log generado."
    msg.attach(MIMEText(message, 'plain'))

    # Ruta del archivo Log_Auditoria
    archivo_a_enviar = "C:/Users/Deimer Yepes/Documents/Pruebas/Log_Auditoria2.txt"

    # Adjuntar el archivo al mensaje
    with open(archivo_a_enviar, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(archivo_a_enviar))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(archivo_a_enviar)}"'
        msg.attach(part)

    # Crear el servidor y enviar el mensaje
    with smtplib.SMTP('smtp.gmail.com:587') as server:
        server.starttls()

        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
            print(f"Correo electrónico enviado a {recipient_emails}")
        except Exception as e:
            print(f"Error: {e}")
