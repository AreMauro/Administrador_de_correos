import re
import imaplib
from emailConection import emailConection


class cuentaDeCorreo:

    def __init__(self, correoElectronico: str,
                    nombreDeUsuario:str,
                    password:str,
                    proveedor:str ="gmail" ,
                    puerto: int =993,
                    puerto_ssl:int=465,
                    smtp: str='smtp.gmail.com'):

        self._correo = correoElectronico

        self._password = password
        
        self._usuario = nombreDeUsuario
        
        
        if any(char.isspace() for char in proveedor) == False and len(proveedor) >= 5:
            self._proveedor = proveedor

        else:
            raise Exception("Error el proveedor no debe contener espacios y debe tener al menos 5 caracteres de longitud")

        if isinstance(puerto, int) == True:
            self._puerto = puerto

        else:
            raise Exception("El puerto debe ser un entero.")

        if isinstance( puerto_ssl, int) == True:
            self._puerto_ssl = puerto_ssl

        else:
            raise Exception("El puerto debe ser un entero.")


        #CREAR UNA FUNCION QUE VALIDE ESTA PARTE USANDO REGEX
        if any(char.isspace() for char in smtp) == False:
            self._smtp = smtp

        else:
            raise Exception("Error el smtp es incorrecto")
        
        self._conexion = emailConection(self._correo, self._password,
                              self._puerto, self._smtp
                              ).getConection()

        
    @property
    def password(self) ->str:

        return self._password

    @property
    def correo(self) -> str:

        return self._correo
        
    @property
    def usuario(self) -> str:

        return self._usuario

    @property
    def proveedor(self) -> str:

        return self._proveedor

    
    @property
    def  puerto(self) -> int:

        return self._puerto
    
    
    @property
    def puerto_ssl(self) -> int:

        return self._puerto_ssl
    
    @property
    def smtp(self) -> str:

        return self._smtp
    

    @staticmethod
    def _verificarCorreo(correo:str) -> bool:

        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

        if re.match(regex, correo):

            return True

        else:

            return False


    @password.setter
    def password(self, Nuevapassword) ->None:

        if any(char.isspace() for char in Nuevapassword) == False and len(Nuevapassword) >=  5:
            
            self._password = Nuevapassword


    @correo.setter
    def correo(self, email) ->None:
        if self._verificarCorreo(email) == True:
            self._correo
        else:
            print("Correo electronico invalido.")
    
    
    @usuario.setter
    def usuario(self, username) ->None:

        if any(char.isspace() for char in username) == False and len(username) >=  5:
            self._usuario = username

    @proveedor.setter
    def proveedor(self, Nuevoproveedor) ->None:

        if any(char.isspace() for char in Nuevoproveedor) == False and len(Nuevoproveedor) >= 5:
            self._proveedor = Nuevoproveedor
    


    @puerto.setter
    def puerto(self, nuevoPuerto) ->None:

        if isinstance(nuevoPuerto, int) == False:

            self._puerto = nuevoPuerto

    @puerto_ssl.setter
    def puerto_ssl(self, nuevoPuerto) -> None:

        self._puerto_ssl = nuevoPuerto
    
    @smtp.setter
    def smtp(self, nuevoSMTP) -> None:

        self._smtp = nuevoSMTP

    def getConection(self) :

        return self._conexion
    
    def closeConection(self) -> tuple:
        
        close = self._conexion.close()[0]

        logout = self._conexion.logout()[0]

        return (close, logout)


    def getEmailsByAddress(self, correo) ->list:

        Status, mensajes = self.getConection().search(None, f'FROM {correo}')

        mensajes = [x for x in mensajes[0].split()]

        return mensajes


    def getAllEmails(self) ->list:

        Status, mensajes = self.getConection().search(None, "ALL")

        mensajes = [x for x in mensajes[0].split()]

        return mensajes

    def getEmailsByDateAndAddress(self, correo: str,
                                fecha: str) -> list:
        """
            OBTIENE LOS MAILS DE UNA DIRECCION DE CORREO ESPECIFICA Y DE UNA FECHA IGUAL O POSTERIOR A FECHA.

        """

        Status, mensajes = self.getConection().search(None, f'FROM {correo} SINCE {fecha}')

        mensajes = [x for x in mensajes[0].split()]

        return mensajes

    def getEmailsBeforeDate(self, fecha: str) -> list:

        """
            OBTIENE SOLO LOS EMAILS ANTERIORES A UNA FECHA ESPECIFICA
        """
        Status, mensajes = self.getConection().search(None, f'BEFORE {fecha}')

        mensajes = [x for x in mensajes[0].split()]

        return mensajes

    def getEmailsAfterDate(self, fecha: str) -> list:

        """
            OBTIENE SOLO LOS EMAILS POSTERIORES A UNA FECHA ESPECIFICA
            
        """

        Status, mensajes = self.getConection().search(None, f'SINCE {fecha}')

        mensajes = [x for x in mensajes[0].split()]

        return mensajes

    def Eliminar_spam(self, proveedor) -> None:

        nuevaconexion = imaplib.IMAP4_SSL(self._smtp, self._puerto)

        nuevaconexion.login(self._correo, self._password)

        mails = nuevaconexion.select(f"[{proveedor}]/Spam")

        Status, mensajes = nuevaconexion.search(None, 'All')

        mensajes = [x for x in mensajes[0].split()]

        MensajesHallados = len(mensajes)

        print(f"\n\nEliminando los correos spam\n\n")

        print(f"Se encontraron {MensajesHallados} mensajes\n")

        mailseliminados = 0

        for mail in mensajes:

            mailseliminados += 1

            nuevaconexion.store(mail,"+FLAGS", "\\Deleted")

            if mailseliminados % 2 == 0:
                
                porcentajeProgreso = (mailseliminados/MensajesHallados)*100

                print(f"Progreso: {round(porcentajeProgreso, 2)}%")
        
        print("Operacion completada!!!")

        nuevaconexion.expunge()

        nuevaconexion.close()

        nuevaconexion.logout()


    def __str__(self):
        return f"Mi cuenta es {self._correo}, con usuario: {self._usuario} y proveedor: {self.proveedor}"

    def __repr__(self):

        cl = self.__class__.__name__

        return f"{cl}[usuario = {self._usuario}, correo = {self._correo}, proveedor = {self.proveedor}]"