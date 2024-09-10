import string as strs
import re

class cuentaDeCorreo:

    def __init__(self, correoElectronico,
                    nombreDeUsuario,
                    password,
                    proveedor):

        if self._verificarCorreo(correoElectronico) == True:

            self._correo = correoElectronico

        else:
             raise Exception("Correo electronico invalido.\nSiga el formato aaaa@example.com")


        if self._verificadordeContrasegna(password) == True:

            self._password = password
        else:
            raise Exception("Error la contraseña no es valida.\n\tLa contraseña debe contener numeros, mayusculas y caracteres especiales.")

        if any(char.isspace() for char in nombreDeUsuario) == False and len(nombreDeUsuario) >= 5:
            self._usuario = nombreDeUsuario
        
        else:
            raise Exception("Error el usuario no debe contener espacios y debe tener al menos 5 caracteres de longitud")

        
        if any(char.isspace() for char in proveedor) == False and len(proveedor) >= 5:
            self._proveedor = proveedor

        else:
            raise Exception("Error el proveedor no debe contener espacios y debe tener al menos 5 caracteres de longitud")


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
    

    @staticmethod
    def _verificadordeContrasegna(contrasegna: str) ->bool:

        if any(char.isdigit() for char in contrasegna) == True and any(char.isupper() for char in contrasegna) == True and any(char.isspace() for char in contrasegna) == False and  any(char in strs.punctuation for char in contrasegna)== True:

           return True
    
        else:
                return False

    @staticmethod
    def _verificarCorreo(correo:str) -> bool:

        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

        if re.match(regex, correo):

            return True

        else:

            return False


    @password.setter
    def password(self, Nuevapassword) ->None:

        if len(Nuevapassword) > 0 and self._verificadordeContrasegna(Nuevapassword) == True:

            self._password = Nuevapassword

        else:
            print("Esta usando espacios o no esta usando numeros, caracteres especiales o mayusculas")
    

    @correo.setter
    def correo(self, email) ->None:
        if _verificarCorreo(email) == True:
            self._correo
        else:
            print("Correo electronico invalido.")
    
    
    @usuario.setter
    def usuario(self, username) ->None:

        if any(char.isspace() for char in username) == False and len(username) >=  5:
            self._usuario = username
        
    @proveedor.setter
    def proveedor(self, proveedor) ->None:

        if any(char.isspace() for char in proveedor) == False and len(proveedor) >= 5:
            self._proveedor = proveedor
        
    def __str__(self):
        return f"Mi cuenta es {self._correo}, con usuario: {self._usuario} y proveedor: {self._proveedor}"
