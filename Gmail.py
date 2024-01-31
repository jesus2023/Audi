import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

#Sin embargo, Google no permitirá el inicio de sesión a través de smtplib 
#porque ha marcado este tipo de inicio de sesión como "menos seguro".
#Para solucionar este problema, vaya a https://www.google.com/settings/security/lesssecureapps
#mientras está conectado a su cuenta de Google y a "Permitir aplicaciones menos seguras".

def correo_exitoso():
    # Configuración del mensaje y credenciales
    sender_email = "jesus.suarez@record.com.co"
    password = "mamona2023"

    # Lista de destinatarios
    recipient_emails = ["jesus.suarez@record.com.co", "anderson.diaz@record.com.co"]

    # Crear instancia del mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(recipient_emails)
    msg['Subject'] = "Archivos adjuntos"

    # Mensaje en formato HTML
    html_content = """
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

    # Adjuntar el contenido HTML al mensaje
    msg.attach(MIMEText(html_content, 'html'))

    # Carpeta que contiene los archivos que deseas adjuntar
    carpeta_con_archivos = "C:/Users/Deimer Yepes/Documents/Documentos de prueba"  # Cambiar la ruta por la solicitada

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
            print(f"Correo electrónico con archivos adjuntos y formato HTML enviado exitosamente a {recipient_emails}")
        except Exception as e:
            print(f"Error: {e}")
