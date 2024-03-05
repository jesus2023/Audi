import os
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

# Configuración
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SENDER_EMAIL = "notificaciones.rpa@record.com.co"  # El correo electrónico del remitente

def get_credentials():
    """Obtiene las credenciales del usuario. Genera el archivo token.json si no existe."""
    creds = None
    token_path = 'C:/Users/RPA/Documents/Proyectos_Rocketbot/Bot Auditoria/Insumos/Auditoria_Python/token.json'
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:/Users/RPA/Documents/Proyectos_Rocketbot/Insumos generales/Gmail Suite/client_secret_72066792837-37grh5ta3rfqdr39qu7muk553criatp3.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def create_message_with_attachment(sender, to, subject, message_text, file_path):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    message.attach(msg)

    # Adjuntar archivo
    with open(file_path, "rb") as file:
        attach = MIMEApplication(file.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=str(file_path))
        message.attach(attach)

    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")}

def send_message_with_attachment(service, sender, to, subject, message_text, file_path):
    try:
        message = create_message_with_attachment(sender, to, subject, message_text, file_path)
        sent_message = service.users().messages().send(userId=sender, body=message).execute()
        print(f"Mensaje con adjunto enviado. ID del mensaje: {sent_message['id']}")
    except HttpError as error:
        print(f'Error al enviar el mensaje: {error}')


def enviar_soporte(timestamp):
    """Función principal."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Detalles del mensaje
    to_email = "soporte.rpa@record.com.co, carlos,perez@record.com.co, reomir.negrete@record.com.co"
    email_subject = "Error en la ejecución del Bot Auditoria BD Python, log generado."
    email_body = "Ha ocurrido un error con en la ejecución del Bot Auditoria BD Python, por favor valide el log generado."
    attachment_path = (f"C:/Users/RPA/Documents/Proyectos_Rocketbot/Bot Auditoria/Insumos/Auditoria_Python/logs/log_file_Auditoría_{timestamp}.log")  # Reemplaza con la ruta del archivo que deseas adjuntar

    send_message_with_attachment(service, SENDER_EMAIL, to_email, email_subject, email_body, attachment_path)

    logging.error(f'Correo enviado a {to_email}')