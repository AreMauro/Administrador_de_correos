from cuentaCorreo import cuentaDeCorreo

class Usuario:

    def __init__(self, username, password):

        if (any(char.isspace for char in username)) == False and len(username) > 5:
            
            self.USERNAME = username
        else:

            raise Exception("")

        if cuentaDeCorreo._verificadordeContrasegna(password) == True and len(password) > 0:

            self._PASS = password

        else:

            print("Contraseña invalida.\nUse caracteres especiale, numeros y mayusculas.")

    @property
    def username(self):

        return self.USERNAME

    @property
    def password(self):

        return self._PASS

    @username.setter
    def username(self, username:str):

        if (any(char.isspace for char in username)) == False and len(username) > 5:
            
            self.USERNAME = username
    
    @password.setter
    def password(self, password: str):

        if cuentaDeCorreo._verificadordeContrasegna(password) == True and len(password) > 0:

            self._PASS = password

        else:

            print("Contraseña invalida.\nUse caracteres especiale, numeros y mayusculas.")

    def __str__():

        return f"Cuenta: {self.USERNAME}"