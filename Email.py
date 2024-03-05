import os
import base64
import logging
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


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

def create_message(sender, to, subject, message_text):
    """Crea un mensaje de correo electrónico."""
    message = f"From: {sender}\nTo: {to}\nSubject: {subject}\n\n{message_text}"
    raw_message = base64.urlsafe_b64encode(message.encode("utf-8")).decode("utf-8")
    return {"raw": raw_message}

def send_message(service, sender, to, subject, message_text):
    """Envía un mensaje de correo electrónico."""
    try:
        message = create_message(sender, to, subject, message_text)
        sent_message = service.users().messages().send(userId=sender, body=message).execute()
        print(f"Mensaje enviado. ID del mensaje: {sent_message['id']}")
    except HttpError as error:
        print(f'Error al enviar el mensaje: {error}')

def enviar_cliente():
    """Función principal."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Detalles del mensaje
    to_email = "soporte.rpa@record.com.co, jesus.suarez@record.com.co, carlos.perez@record.com.co"
    email_subject = "Error en la ejecucion del Bot Auditoria BD Python"
    email_body = "Ha ocurrido un error con la ejecución del Bot Auditoria BD Python, por favor realice el proceso de consulta y generación de archivos de forma manual."

    send_message(service, SENDER_EMAIL, to_email, email_subject, email_body)
    logging.info(f'Correo enviado a {to_email}')

