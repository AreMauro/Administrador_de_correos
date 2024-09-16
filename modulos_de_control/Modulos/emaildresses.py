from pathlib import Path

from tempfile import NamedTemporaryFile, mkdtemp

from shutil import rmtree

from cuentaCorreo import cuentaDeCorreo

from Email import Email
 
import imaplib

from DatosConexion import (
                            Carga_de_Datos)

from pprint import pprint

from Utilerias import (
                    Mensajes, 
                    clear)

from json import dump, load

from json.decoder import JSONDecodeError

from traceback import print_exc

Raiz = Path(".")

def CrearArchivosTemporales() -> tuple:

    """
    Crea los archivos temporales que se utilizan para almacenar las direcciones de correo que no son considerados como 

    """

    print("Creando...")

    DireccionesAlmacenadas = Path(
                    Raiz, 
                    "Datos\\Direcciones de correo")

    CorreosValidos= Path(
                    Raiz, 
                    "Datos\\Direcciones de correo\\Direcciones Validas.json")


    if DireccionesAlmacenadas.exists() == False:

        DireccionesAlmacenadas.mkdir()

        CorreosValidos.touch()
    
    else:

        if CorreosValidos.is_file() == False:

            CorreosValidos.touch()

    return (CorreosValidos,)

def Cargar_Datos(arch : Path) -> tuple:

    try:
        
        with open(arch, "r") as JsonFile:

            Datos_Antiguos = load(JsonFile)
        
        return (Datos_Antiguos, Mensajes[7])

    except JSONDecodeError:

        return ("", )

    except:

        return (Mensajes[5], )

def Direccion_valida(correo: bytes) -> bool:

    print(f"La direccion {correo} es util ?")
    
    valido = False

    while valido == False:
        
        Ans = input(Mensajes[3])

        if Ans == "":

            print(Mensajes[4])

            valido = False
        
        else:

            if Ans.upper() == "Y":

                return True
            
            elif Ans.upper() == "N":

                return False
            
            else:

                print(Mensajes[6])

                valido = False

def direcciones_existentes() -> dict:

    direcciones = Path(Raiz, 
                    "Datos\\direccioneValidas.json")

    if direcciones.is_file() == True:

        patrones = Cargar_Datos(direcciones)
        
        if patrones[0] == "":

            return {}

        if patrones[1] == Mensajes[7]:

            return patrones[0]
    
    else:

        return {}

def Clasificar_mails(correo: str
                     ) -> bool:

    Direcciones = direcciones_existentes()

    if len(Direcciones) == 0:

        return False
    
    else:

        for nombre in Direcciones.values():

            if correo == nombre == True:

                return True
    
    return False

def Clasificacion(Direcciones: set,
                  correos_validos: set) -> set:

    for email in Direcciones:

        invalides = Clasificar_mails(email)

        if invalides == True:

            continue;
                
        elif invalides == False:
                
            if email in correos_validos:

                continue;

            valides = Direccion_valida(email)

            if valides == True:

                correos_validos.add(email)
            
    return correos_validos

def Obtener_direcciones_validas(cuenta:cuentaDeCorreo) -> set:
    
    try:
        print("Obteniendo direcciones...")

        Direcciones = set()

        correos_validos = set()

        print("Conectando...")

        print("Buscando...")

        emails = cuenta.getAllEmails()

        last_email_id = int(emails[-1]) + 1

        print(f"Se encontraron {last_email_id} mails")

        contadormails = 0

        for email in emails:

            emailActual = Email(cuenta, email)

            nombre = emailActual.getSender()

            Direcciones.add(nombre)
        
            contadormails += 1
            
            print(contadormails)

            if contadormails % 200 == 0:
                
                print("Clasificando...")

                correos_validados = Clasificacion(Direcciones,
                                                  correos_validos)

                Direcciones.clear()

                print(f"Progreso: {round((contadormails/last_email_id)*100)}%...")

        print(Mensajes[7])

        print("Cerrando sesion...")

        pprint(correos_validados)

        return correos_validos
    
    except:
        
        print_exc()

        return [Mensajes[5]]


def crear_dict(correos_validos: set, 
               inicio: int = 0) -> dict:

    Datos = list(correos_validos)

    dictDatos = {str(inicio + i) : Datos[i] 
                for i in range(len(Datos))}

    return dictDatos

def Actualizar_Datos(correos_validos: dict) -> str:

    Base_de_datos = CrearArchivosTemporales()

    try:

        print("\nAgregando contenido al archivo...\n")

        with open(Base_de_datos[0], "w") as JsonFile:

            dump(correos_validos, JsonFile,
                indent="\n\t", 
                sort_keys = True)

            return Mensajes[7]

    except:

        print_exc()

        return Mensajes[5]
        

def Eliminar_Archivos_Temporales(
                    Destino: Path) ->None:
    
    try:
        
        rmtree(Destino)

        return Mensajes[7]
    
    except FileNotFoundError:

        print ("El archivo no existe...")

        return Mensajes[7]
    
    except:

        return Mensajes[5]

def Actualizar_direcciones_validas(cuenta:cuentaDeCorreo) -> None :

    DireccionesAlmacenadas = Path(
                    Raiz, 
                    "Datos\\Direcciones de correo")

    Eliminar_Archivos_Temporales(DireccionesAlmacenadas)

    Datos = Obtener_direcciones_validas(cuenta)

    pprint(Datos)

    nuevos_validos = crear_dict(Datos)

    pprint(nuevos_validos)

    Estado_actualizacion = Actualizar_Datos(nuevos_validos)

    
    if (Datos != Mensajes[6] and 
        Estado_actualizacion != Mensajes[7]):

        print(Mensajes[7])

    else:

        print(Mensajes[5])


def Clasificacion2(Spam: Path,
                   Direcciones: set,
                   cuenta:cuentaDeCorreo) -> str:

    CorreosValidos= Path(
                    Raiz, 
                    "Datos\\Direcciones de correo\\Direcciones Validas.json")

    if CorreosValidos.is_file() == False:
        
        Actualizar_direcciones_validas(cuenta)


    Dictvalidos = Cargar_Datos(CorreosValidos)

    if Dictvalidos[0] != "":

        for email in Direcciones:
            
            if email not in Dictvalidos[0].values() and email is not None:

                with open(Spam, "ab+") as sp:
                        
                    sp.write(bytes(email, "utf8"))

                    sp.write(b"\n")
                
        return Mensajes[7]
    
    else:

        return Mensajes[5]

def Obtener_correos_spam(cuenta:cuentaDeCorreo) -> tuple:
    
    try:
        print("Obteniendo direcciones...")
        
        print("Creando archivos temporales...")

        Direcciones = set()

        Aqui = Path(Raiz, "Datos\\")

        Dir = mkdtemp(dir=Aqui)

        Destino = Path(str(Dir))

        Spam = NamedTemporaryFile(
                mode="ab+", dir=Destino, 
                prefix="spam",
                delete=False)

        emails = cuenta.getAllEmails()

        last_email_id = int(emails[-1]) + 1

        print(f"Se encontraron {last_email_id} mails")

        contadormails = 0

        for email in emails:

            emailActual = Email(cuenta, email)

            direccion = emailActual.getSender()

            Direcciones.add(direccion)

            contadormails += 1

            print(contadormails)
   
            if contadormails % 200 == 0:
                
                print("Clasificando...")

                direcciones_Spam = Path(Spam.name)
                
                Estado = Clasificacion2(direcciones_Spam, 
                    Direcciones,
                    cuenta)

                Direcciones.clear()

                clear()

                print(f"Progreso: {round((contadormails/last_email_id)*100)}%...")

        print(Mensajes[7])

        print("Cerrando sesion...")

        return (Spam.name,)
    
    except KeyboardInterrupt: 

        print(Mensajes[8])

    except:
        
        print_exc()
        return (Mensajes[5],)


