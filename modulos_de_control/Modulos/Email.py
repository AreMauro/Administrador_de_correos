import imaplib
import email
from email.header import decode_header
from cuentaCorreo import cuentaDeCorreo
import os
from pathlib import Path
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from traceback import print_exc
from pathlib import Path 


class Email():

    def __init__(self, cuenta: cuentaDeCorreo, mailNumber: bytes =0):

        if isinstance(mailNumber, bytes) ==  True:
            self._number = mailNumber

        if isinstance(cuenta, cuentaDeCorreo) == True:
            self._cuenta = cuenta


    def EliminarEmail(self) -> bool:
        
        try:
            
            conexion = self._cuenta.getConection()

            conexion.store(self._number,"+FLAGS", "\\Deleted")

            conexion.expunge()

            conexion.close()

            conexion.logout()

            return True

            
        except:

            return False

    
    def descargarContenido(self, directorio: str) -> bool:

        try:        
            if 'descargas_de_emails' not in os.listdir(directorio):
                
                Path(directorio + "\\" + "descargas_de_emails" ).mkdir(parents=True, exist_ok=True)
            
            conexion = self._cuenta.getConection()

            typ, messageParts = conexion.fetch(self._number, '(RFC822)')
            emailBody = messageParts[0][1]
            raw_email_string = emailBody.decode('utf-8')
            mail = email.message_from_string(raw_email_string)#
            print('emailbody complete ...')
            for part in mail.walk():
                fileName = part.get_filename()
                print('file names processed ...')
            if bool(fileName):
                filePath = os.path.join(directorio, 'descargas_de_emails', fileName)
                if not os.path.isfile(filePath):
                    print(fileName)
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
                    print('fp closed ...')
            
            conexion.close()

            conexion.logout()

            return True
        
        except: return False

    
    
    def Plantilla_para_archivos_propios(self, 
                Archivos:list) -> str:

        Raiz = ".\\Datos\\Plantillas"

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


    def CrearMensajeConArchivoAdjuntos(self, plantilla: str,
                  Directorio: Path,
                  reciber_email: str,
                  subject: str,
                  Archivos: list):
        

            mensaje = MIMEMultipart()

            mensaje["From"] = self._cuenta.correo

            mensaje["To"] = reciber_email

            mensaje["Subject"] = subject
            
            Parte1 = MIMEText(plantilla, 'html')

            mensaje.attach(Parte1)


            for filename in Archivos:

                    Ruta = Path(Directorio,filename)

                    print(filename)

                    with open(Ruta, "rb") as attachment:
                
                        part = MIMEBase("application", "octet-stream")
                        
                        part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)

                        part.add_header(
                                "Content-Disposition",
                        f"attachment; filename= {filename}",)

                        mensaje.attach(part)
            
            return (mensaje, reciber_email)

    def Enviar_mail(self, reciber_email: str,
                subject: str,
                directorioArchivos: str):

        try:

            Carpeta_archivos = Path(directorioArchivos)
            
            Archivos_para_enviar = Carpeta_archivos.iterdir()

            nombre_archivos = [str(Archivo).split("\\")[-1]
                        for Archivo
                        in list(Archivos_para_enviar)]

            plantilla = self.Plantilla_para_archivos_propios(nombre_archivos)

            mensaje = self.CrearMensajeConArchivoAdjuntos(plantilla,
                                    Carpeta_archivos,
                                    reciber_email,
                                    subject,
                                    nombre_archivos)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(self._cuenta.smtp, self._cuenta.puerto_ssl, context=context) as server:

                server.login(self._cuenta.correo, 
                              self._cuenta.password)

                server.sendmail(self._cuenta.correo, 
                                mensaje[1], 
                                mensaje[0].as_string())


        except:
                print_exc()


    def getSender(self) ->str:

        conexion = self._cuenta.getConection()

        typ, data = conexion.fetch(self._number,'(RFC822)')

        if data is not None:
            
            try:

                msg = email.message_from_bytes(data[0][1])
            
                From, encoding = decode_header(msg.get("From"))[0]
            
                if isinstance(From, bytes):
                    From = From.decode()  
        
                Sender = email.utils.parseaddr(From)[1] 

                if Sender.find("@") != -1:  
                    
                    conexion.close()

                    conexion.logout()

                    return Sender

                else: 

                    
                    conexion.close()

                    conexion.logout()
                    
                    return None
                
            except TypeError:

                conexion.close()

                conexion.logout()
                    
                return None
                


        else:

            
            conexion.close()

            conexion.logout()
                        
            return None
    

