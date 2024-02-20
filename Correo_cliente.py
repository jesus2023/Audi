from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTPException
import os
from dotenv import load_dotenv
import logging

def enviar_cliente():

    # Carga las variables de entorno desde el archivo email.env
    load_dotenv("C:/Users/RPA/Desktop/Audi/Gmail/email.env")

    # Accede a las variables de entorno
    sender_email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    # Lista de destinatarios
    recipient_emails = ["jhovanna.lopez@record.com.co"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = "Error en la ejecución del Bot Auditoria BD"

    message = "Ha ocurrido un error con la ejecución del Bot Auditoria BD, por favor realice el proceso de consulta y generación de archivos de forma manual."

    msg.attach(MIMEText(message, 'plain'))

    # Crear el servidor y enviar el mensaje
    with smtplib.SMTP('smtp.gmail.com:587') as server:
        server.starttls()

        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
            print(f"Correo electrónico enviado a {recipient_emails}")
            logging.error(f'Correo enviado a {recipient_emails}')
        except SMTPException as e:
            print(f"Error durante el envío del correo: {e}")
            logging.error('Correo no enviado')
