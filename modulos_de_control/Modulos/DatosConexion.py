from pathlib import Path
from json import dump, load
from Utilerias import (
                        Pedir_informacion,
                        Autorizacion, 
                        Mensajes)

Dir = Path("C:\\Users\\Ivan\\Downloads\\Desktop\\Proyectos\\Administrador de Emails\\modulos_de_control\\Modulos\\Datos\\Credenciales.json")

def Captura_de_datos(proveedor: str, 
                    username: str) -> dict:

    
    if proveedor.upper() == "GMAIL":

        password = Pedir_informacion(Mensajes[1])

        correo = Pedir_informacion(Mensajes[2])

        Datos = {username :
            
                    {
                        'puerto' : '993',

                        'proveedor': 'imap.gmail.com',

                        'password' : password,

                        'username' : correo,

                        'smtp' : 'smtp.gmail.com',

                        'puerto_ssl' : 465
                                
                                }
                                    }

        return Datos

    
    else:

        return {1: ""}

def Guardado_De_datos(username: str) -> str:

    try:

        proveedor = Pedir_informacion(Mensajes[17]) 
        
        credenciales = Captura_de_datos(proveedor, 
                                        username)

        while (1 in credenciales.keys()) == True:

            print(Mensajes[6])

            proveedor = Pedir_informacion(Mensajes[17]) 

            credenciales = Captura_de_datos(proveedor, 
                                        username)

        if Dir.is_file() == False:

            with open(Dir, "w") as f:

                dump(credenciales,f,
                    indent="\n\t", 
                    sort_keys = True)
            
            return Mensajes[7]
        else:

            with open(Dir, "r") as F:

                Datos = load(F)

            Datos.update(credenciales)

            with open(Dir, "w") as f:

                dump(Datos,f,
                    indent="\n\t", 
                    sort_keys = True)

            return Mensajes[7]

    except KeyboardInterrupt:

        print(Mensajes[8])

        quit()

def Carga_de_Datos(username: str) -> dict:
    """
    Esta funcion toma los datos del archivo que contiene los datos y los depura
    
    SHALLALALALALLALALA
    """
    try:

        if Dir.is_file() == True:

            with open(Dir, "r") as F:

                Datos = load(F)
                    
            if username in Datos.keys():

                return Datos[username]

            else:

                print(Mensajes[15])

                peticion = Autorizacion(Mensajes[16])

                if peticion == "Y":
                
                    Estado = Guardado_De_datos(username)

                    return {1 : Estado}

                else:

                    return {1: ""}

        else:

            Estado = Guardado_De_datos(username)

            return {1 : Estado}
    
    except KeyboardInterrupt:
        
        print(Mensajes[8])

        quit()

def Actualizar_credenciales():
    
    Respuesta = Autorizacion("S")

    if Respuesta.upper() == "Y":
            
        credenciales = Captura_de_datos()

        with open(Dir, "w") as f:

            dump(credenciales,f,
                    indent="\n\t", 
                    sort_keys = True)
                
        return 1

    elif Respuesta.upper() == "N":

        return 1
        
    else:

        print(Mensjes[5])

        quit()


def Añadir_cuenta():
    
    Actualizar_credenciales()