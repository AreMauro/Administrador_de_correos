import imaplib

class emailConection():

    _instance = None

    def __new__(cls, correo: str,
                    password:str,
                    puerto: int =993,
                    smtp: str='smtp.gmail.com',
                    *args, **kwargs):

        if not cls._instance:
        
            cls._instance = super().__new__(cls, *args, **kwargs)
        
        return cls._instance
    
    def __init__(self, correo: str,
                    password:str,
                    puerto: int =993,
                    smtp: str='smtp.gmail.com') -> None:

        self._smtp = smtp

        self._correo = correo

        self._password = password
    
        if isinstance(puerto, int) == True:

            self._puerto = puerto

        else:
            raise Exception("El puerto debe ser un entero.")
        

        self.nuevaconexion = imaplib.IMAP4_SSL( self._smtp, self._puerto)
        
        self.nuevaconexion.login(self._correo, self._password)

        conexion = self.nuevaconexion.select("INBOX")


    
    @property
    def password(self) ->str:

        return self._password

    @property
    def correo(self) -> str:

        return self._correo
        
    @property
    def  puerto(self) -> int:

        return self._puerto
    
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


    @puerto.setter
    def puerto(self, nuevoPuerto) ->None:

        if isinstance(nuevoPuerto, int) == False:

            self._puerto = nuevoPuerto
    
    @smtp.setter
    def smtp(self, nuevoSMTP) -> None:

        self._smtp = nuevoSMTP

    
    def getConection(self) -> imaplib.IMAP4_SSL:

        return self.nuevaconexion
    