import string as strs

class Usuario:

    def __init__(self, username, password):

        
        self._username = username
        self._PASS = password

    @property
    def username(self) -> str:

        return self._username

    @property
    def password(self) -> str:

        return self._PASS

    @staticmethod
    def _verificadordeContrasegna(contrasegna: str) ->bool:

        if any(char.isdigit() for char in contrasegna) == True and any(char.isupper() for char in contrasegna) == True and any(char.isspace() for char in contrasegna) == False and  any(char in strs.punctuation for char in contrasegna)== True:

           return True
    
        else:
                return False

    @username.setter
    def username(self, username:str) -> None:

        if (any(char.isspace() for char in username)) == False and len(username) > 5:
            
            self._username = username
    
    @password.setter
    def password(self, password: str) -> None:

        if self._verificadordeContrasegna(password) == True and len(password) > 10:

            self._PASS = password

        else:

            print("Contraseña invalida.\nUse caracteres especiale, numeros y mayusculas y la longitud debe ser de 10 o mas caracteres")

    def __str__(self):

        return f"Cuenta: {self._username}"
    
    def __repr__(self):
        cl = self.__class__.__name__
        return f"{cl}: usuario = {self._username}"