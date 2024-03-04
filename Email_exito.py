import os
import base64
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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

def create_message_with_folder(sender, to, subject, html_content, folder_path, cc=None, bcc=None):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    if cc:
        message['cc'] = cc
    if bcc:
        message['bcc'] = bcc

    # Crear la parte del cuerpo HTML y adjuntarla al mensaje
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)

    # Obtener la lista de archivos en la carpeta
    archivos_en_carpeta = os.listdir(folder_path)

    # Adjuntar cada archivo al mensaje
    for archivo in archivos_en_carpeta:
        archivo_path = os.path.join(folder_path, archivo)
        if os.path.isfile(archivo_path):
            with open(archivo_path, "rb") as file:
                attach = MIMEApplication(file.read(), Name=os.path.basename(archivo))
                attach.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(archivo)}"')
                message.attach(attach)

    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")}



def send_message_with_attachment(service, sender, to, subject, message_text, attachment_path, html_content):
    try:
        if os.path.isdir(attachment_path):
            # Si el path es un directorio, utiliza la función existente
            message = create_message_with_folder(sender, to, subject, message_text, attachment_path, html_content)
        else:
            # Si no es un directorio, imprime un mensaje de error
            print(f'Error: El path especificado no es un directorio: {attachment_path}')
            return

        sent_message = service.users().messages().send(userId=sender, body=message).execute()
        print(f"Mensaje con adjunto(s) y contenido HTML enviado. ID del mensaje: {sent_message['id']}")
    except HttpError as error:
        print(f'Error al enviar el mensaje: {error}')

def correo_exitoso():
    """Función principal."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Detalles del mensaje
    to_email = "reomir.negrete@record.com.co, jhovanna.lopez@record.com.co"
    cc_email = "kevis.mercado@record.com.co"
    bcc_email = "soporte.rpa@record.com.co"
    email_subject = "Bot Auditoria Python Ejecutado exitosamente"   
    
    # Contenido HTML
    email_body =  """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Correo HTML</title>
        <style>
            .mensaje {
                color: rgb(0, 0, 0);
                font-weight: 800;
                font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
                font-size: 20px;
            }
            .slogan {
                color: rgb(12, 182, 40);
                font-weight: 800;
                font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
            }
            .firma {
                color: red;
                font-weight: 800;
                font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
            }
            .bot img {
                width: 150px;
            }
        </style>
    </head>
    <body>
        <p class="mensaje">Bot Auditoria_BD: Saldo tesorería ejecutado exitosamente</p><br><br>
        <div class="bot"><img src="http://revistafibra.info/wp-content/uploads/2015/12/bottraffic.jpg" alt="bot"></div>
        <p class="slogan">"Lo hacemos fácil para hacerte feliz en donde quiera que estés"</p>
        <p class="firma">RPA - RECORD</p>
    </body>
    </html>
    """
    
    # Carpeta que contiene los archivos que deseas adjuntar
    attachment_path = "C:/Users/RPA/Documents/Proyectos_Rocketbot/Bot Auditoria/Insumos/Auditoria_Python/Email"  # Cambiar la ruta por la solicitada

    # Modificar la llamada a create_message_with_folder para pasar el contenido HTML primero
    message = create_message_with_folder(SENDER_EMAIL, to_email, email_subject, email_body, attachment_path, cc_email, bcc_email)

    # Enviar el mensaje
    sent_message = service.users().messages().send(userId=SENDER_EMAIL, body=message).execute()
    print(f"Mensaje con adjunto(s) y contenido HTML enviado. ID del mensaje: {sent_message['id']}")

    logging.info(f'Correo enviado a {to_email}')