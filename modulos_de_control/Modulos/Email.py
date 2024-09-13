import imaplib
import email
from email.header import decode_header
from cuentaCorreo import cuentaDeCorreo

class Email():

    def __init__(self, mailNumber: bytes, cuenta: cuentaDeCorreo):

        if isinstance(mailNumber, bytes) ==  True:
            self._number = mailNumber

        if isinstance(cuenta, cuentaDeCorreo) == True:
            self._cuenta = cuenta


    def EliminarEmail(self) -> bool:
        
        try:
            nuevaconexion = imaplib.IMAP4_SSL( self._cuenta.smtp, self._cuenta.puerto)

            nuevaconexion.login(self._cuenta.correo, self._cuenta.password )

            mails = nuevaconexion.select("INBOX")

            nuevaconexion.store(self._number,"+FLAGS", "\\Deleted")

            nuevaconexion.expunge()
    
            nuevaconexion.close()

            nuevaconexion.logout()

            return True

            
        except:

            return False

        
        


    
    def descargarContenido(self) -> bool:
        
        pass
    
    def sendEmail(self) -> bool:
        pass 

    def getSender(self) ->str:

        nuevaconexion = imaplib.IMAP4_SSL( self._cuenta.smtp, self._cuenta.puerto)
        
        nuevaconexion.login(self._cuenta.correo, self._cuenta.password)

        conexion = nuevaconexion.select("INBOX")

        typ, data = nuevaconexion.fetch(self._number,'(RFC822)')
        
        msg = email.message_from_bytes(data[0][1])
        
        From, encoding = decode_header(msg.get("From"))[0]
        
        if isinstance(From, bytes):
            From = From.decode()  
        
        Sender = email.utils.parseaddr(From)[1]    
        
        nuevaconexion.close()
        
        return Sender    
        


