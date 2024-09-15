from pathlib import Path

from tempfile import NamedTemporaryFile, mkdtemp

from shutil import rmtree

import email

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

Raiz = Path("C:\\Users\\Ivan\\Downloads\\Desktop\\Proyectos\\Administrador de Emails\\modulos_de_control\\Modulos")

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

    print(f"La direccion {str(correo, 'utf-8')} es util ?")
    
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
                    "Datos\\Patrones.json")

    if direcciones.is_file() == True:

        patrones = Cargar_Datos(direcciones)
        
        if patrones[0] == "":

            return {}

        if patrones[1] == Mensajes[7]:

            return patrones[0]
    
    else:

        return {}

def Clasificar_mails(correo: bytes, 
                     Nuevos_patterns: list
                     ) -> bool:

    Direcciones = direcciones_existentes()

    if len(Direcciones) == 0:

        return False
    
    else:


        for pattern in Direcciones.values():

            if correo.find(bytes(pattern, "utf-8")) != -1:

                return True
        
        for pattern in set(Nuevos_patterns):

            if correo.find(pattern) != -1:

                return True
    
    return False


def Depurar_mail(texto: bytes) -> bytes:

    if (b"<" in texto and 
        b">" in texto):

        inicio = texto.find(b"<") + 1

        final = texto.find(b">",
                        inicio)
        
        email = texto[inicio : final]

        return email
    
    return texto


def Clasificacion(Direcciones: set, 
                  patrones_nuevos: list,
                  correos_validos: set) -> list:

    for email in Direcciones:
            
        email_depurado = Depurar_mail(email)

        invalides = Clasificar_mails(email_depurado, 
            patrones_nuevos)

        if invalides == True:

            continue;
                
        elif invalides == False:
                
            if email_depurado in correos_validos:

                continue;

            valides = Direccion_valida(email_depurado)

            if valides == True:

                correos_validos.add(email_depurado)
                
            else:

                inicio = email_depurado.find(b"@")

                patron = email_depurado[inicio:]

                print(patron)

                patrones_nuevos.append(patron)

                continue;

    return [patrones_nuevos, correos_validos]

def Obtener_direcciones_validas(
                        Claves: dict) -> list:
    
    try:
        print("Obteniendo direcciones...")

        Direcciones = set()

        patrones_nuevos = []

        correos_validos = set()

        print("Conectando...")

        nuevaconexion = imaplib.IMAP4_SSL(Claves["proveedor"],Claves["puerto"])

        nuevaconexion.login(Claves["username"], Claves["password"])

        nuevaconexion.select("INBOX")

        print("Buscando...")

        data = nuevaconexion.search(None, "ALL")

        mail_ids = data[1]

        id_list = mail_ids[0].split()

        first_email_id = int(id_list[0])

        last_email_id = int(id_list[-1]) + 1

        print(f"Se encontraron {last_email_id} mails")

        contadormails = 0

        for i in range (first_email_id, last_email_id):

            data = nuevaconexion.fetch(
                            str(i),"(RFC822)")
            
            for response_part in data:

                arr = response_part[0]
                
                if isinstance(arr, tuple):

                    inicio_direccion = arr[1].find(b"From: ") + len(b"From: ")
                    
                    final_direccion = arr[1].find(b"\r\n", inicio_direccion)    

                    texto_crudo = arr[1][inicio_direccion:final_direccion]
                    
                    if b"@" in texto_crudo:
                        
                        Direcciones.add(texto_crudo)

                    contadormails += 1
            
            if contadormails % 200 == 0:
                
                print("Clasificando...")

                patrones, correos_validados = Clasificacion(Direcciones,
                    patrones_nuevos,
                    correos_validos)

                Direcciones.clear()

                print(f"Progreso: {round((contadormails/last_email_id)*100)}%...")

        print(Mensajes[7])

        print("Cerrando sesion...")

        nuevaconexion.close()

        nuevaconexion.logout()

        Patrones = set(patrones_nuevos)

        pprint(patrones)

        print("\n")

        pprint(correos_validados)

        return [correos_validos, Patrones]
    
    except:
        
        print_exc()

        nuevaconexion.close()

        nuevaconexion.logout()

        return [Mensajes[5]]


def crear_dict(correos_validos: set, 
               inicio: int = 0) -> dict:

    Datos = list(correos_validos)

    dictDatos = {str(inicio + i) : str(Datos[i], "utf-8") 
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
        

def Actualizar_patrones(patrones_nuevos: dict) -> bool:

    try:

        direcciones = Path(Raiz, 
                        "Datos\\Patrones.json")

        patrones_actuales = direcciones_existentes()

        if len(patrones_actuales) != 0:
            
            dictPatronesNuevos = crear_dict(patrones_nuevos, len(patrones_actuales))

            patrones_actuales.update(dictPatronesNuevos)

            with open(direcciones, "w") as JsonFile:

                    dump(patrones_actuales, JsonFile,
                    indent="\n\t", 
                    sort_keys = True)

            return Mensajes[7]

        else:

            with open(patrones_nuevos, "w") as JsonFile:

                    dump(patrones_para_agregar, JsonFile,
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

        print ("El archivo ya fue eliminado...")

        return Mensajes[7]
    
    except:

        return Mensajes[5]

def Actualizar_direcciones_validas(Claves: dict) -> None :

    DireccionesAlmacenadas = Path(
                    Raiz, 
                    "Datos\\Direcciones de correo")

    Eliminar_Archivos_Temporales(DireccionesAlmacenadas)

    Datos = Obtener_direcciones_validas(Claves)

    pprint(Datos)

    nuevos_validos = crear_dict(Datos[0])

    pprint(nuevos_validos)

    Estado_actualizacion = Actualizar_Datos(nuevos_validos)

    estado_actualizar_patrones = Actualizar_patrones(Datos[1])
    
    
    if (Datos != Mensajes[6] and 
        Estado_actualizacion != Mensajes[7] and 
        estado_actualizar_patrones == Mensajes[7]):

        print(Mensajes[7])

    else:

        print(Mensajes[5])


def Clasificacion2(Spam: Path,
                   Direcciones: set) -> str:

    CorreosValidos= Path(
                    Raiz, 
                    "Datos\\Direcciones de correo\\Direcciones Validas.json")

    if CorreosValidos.is_file() == False:

        return Mensajes[5]

    Dictvalidos = Cargar_Datos(CorreosValidos)

    if Dictvalidos[0] != "":

        for email in Direcciones:
            
            email_depurado = Depurar_mail(email)

            if str(email_depurado, "utf-8") not in     Dictvalidos[0].values():

                with open(Spam, "ab+") as sp:
                        
                    sp.write(email_depurado)

                    sp.write(b"\n")
                
        return Mensajes[7]
    
    else:

        return Mensajes[5]

def Obtener_correos_spam() -> tuple:
    
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
    


        first_email_id = int(id_list[0])

        last_email_id = int(id_list[-1]) + 1

        print(f"Se encontraron {last_email_id} mails")

        contadormails = 0

        for i in range (first_email_id, last_email_id):

            data = nuevaconexion.fetch(
                            str(i),"(RFC822)")
            
            for response_part in data:

                arr = response_part[0]
                
                if isinstance(arr, tuple):

                    inicio_direccion = arr[1].find(b"From: ") + len(b"From: ")
                    
                    final_direccion = arr[1].find(b"\r\n", inicio_direccion)    

                    texto_crudo = arr[1][inicio_direccion:final_direccion]
                    
                    if b"@" in texto_crudo:
                        
                        Direcciones.add(texto_crudo)

                    contadormails += 1
            
            if contadormails % 200 == 0:
                
                print("Clasificando...")

                direcciones_Spam = Path(Spam.name)
                
                Estado = Clasificacion2(direcciones_Spam, 
                    Direcciones)

                if Estado != Mensajes[7]:

                    print(Mensajes[5] + "\nPor favor actualice el archivo de correos validos.")

                    break;

                Direcciones.clear()

                clear()

                print(f"Progreso: {round((contadormails/last_email_id)*100)}%...")

        print(Mensajes[7])

        print("Cerrando sesion...")

        nuevaconexion.close()

        nuevaconexion.logout()

        return (Spam.name,)
    
    except KeyboardInterrupt: 

        print(Mensajes[8])

    except:
        
        print_exc()

        nuevaconexion.close()

        nuevaconexion.logout()

        return (Mensajes[5],)


