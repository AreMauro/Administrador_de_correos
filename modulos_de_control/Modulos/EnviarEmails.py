import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pathlib import Path 

from modulos_de_control.Modulos.DatosConexion import (
                            Carga_de_Datos)

from traceback import print_exc

from modulos_de_control.Modulos.Utilerias import (
                            clear)

from pprint import pprint

def Plantilla_para_archivos_propios(
                Archivos:list) -> str:

    Raiz = "C:\\Users\\Ivan\\Downloads\\Desktop\\Proyectos\\Administrador de Emails\\modulos_de_control\\Modulos\\Datos\\Plantillas"

    Plantilla = Path(Raiz, "Plantilla_1.html")

    html = Plantilla.open().read()

    Inicio  = html.find("</h3>") - len("</h3>")

    plantilla = html[ : Inicio]

    plantilla += "\n\n\t<ol style=\"list-style-type: upper-roman;\">"

    formato = "\n\n\t\t<li>\n\n\t\t\t{Archivo}\n\n\t\t</li>"

    nombre_archivos_en_email = [
                        formato.format(
                    Archivo = str(Archivo).split("\\")[-1]) 
                    for Archivo
                    in Archivos]

    plantilla += "".join(nombre_archivos_en_email)

    plantilla += "\n\n\t</ol>\n"

    plantilla += html[Inicio: ]

    return plantilla


def Crear_mensaje(plantilla: str,
                  Directorio: Path,
                  Archivos: list,
                  reciber_email: str,
                  subject: str, 
                  Claves: dict):
    try:

        mensaje = MIMEMultipart()

        mensaje["From"] = Claves["username"]

        mensaje["To"] = reciber_email

        mensaje["Subject"] = subject
        
        Parte1 = MIMEText(plantilla, 'html')

        mensaje.attach(Parte1)

        for filename in Archivos:

                Ruta = Path(Directorio,filename)

                with open(Ruta, "rb") as attachment:
            
                    part = MIMEBase("application", "octet-stream")
                    
                    part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)

                    part.add_header(
                            "Content-Disposition",
                    f"attachment; filename= {filename}",)

                    mensaje.attach(part)
        
        return (mensaje, reciber_email)

    except:

        print("Error")


def Enviar_mail(reciber_email: str,
                subject: str,
                Claves: dict):

    try:

        Carpeta_archivos = Path("C:\\Users\\Ivan\\Downloads\\Desktop\\Envios")
        
        Archivos_para_enviar = Carpeta_archivos.iterdir()

        nombre_archivos = [str(Archivo).split("\\")[-1]
                    for Archivo
                    in list(Archivos_para_enviar)]

        plantilla = Plantilla_para_archivos_propios(nombre_archivos)

        mensaje = Crear_mensaje(plantilla,
                                Carpeta_archivos,
                                nombre_archivos,
                                reciber_email,
                                subject,
                                Claves)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(Claves["smtp"], Claves["puerto_ssl"], context=context) as server:

            server.login(Claves["username"], 
                         Claves["password"])

            server.sendmail(Claves["username"], 
                            mensaje[1], 
                            mensaje[0].as_string())


    except:
            print_exc()
