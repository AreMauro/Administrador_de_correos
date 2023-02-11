from imbox import Imbox

import os

from pathlib import PurePath

from modulos_de_control.Modulos.DatosConexion import (
                                Carga_de_Datos)

from modulos_de_control.Modulos.emaildresses import (
                            Cargar_Datos)

from pathlib import Path

from modulos_de_control.Modulos.Utilerias import (
                                clear, 
                                Mensajes)

def Descargardor(Correo: str,
                Claves: dict) -> None:

    Folder_destino = PurePath("C:\\Users\\Ivan\\Downloads\Desktop\\Descargas")

    mail = Imbox(Claves["proveedor"], username=Claves["username"], password=Claves["password"], ssl = True, ssl_context = None, starttls=False)

    messages = mail.messages(sent_from = Correo)


    for (uid, mensaje) in messages:

        for idx, attachment in enumerate(mensaje.attachments):

            att_fn = attachment.get("filename")

            print(f"Descargando {att_fn} en {Folder_destino}")
            
            DirDESCARGA = str(Folder_destino)+"\\"+att_fn
            
            with open(DirDESCARGA,"wb") as recibo:

                recibo.write(attachment.get("content").read())

    mail.logout()

def Descargar_de_direcciones_validas(
                        Claves: dict) -> None:

    Validos = Path("C:\\Users\\Ivan\\Downloads\\Desktop\\Proyectos\\Administrador de Emails\\modulos_de_control\\Modulos\\Datos\\Direcciones de correo\\Direcciones Validas.json")

    Direcciones = Cargar_Datos(Validos)

    if (Direcciones[0] != "" and 
        Direcciones[0] != Mensajes[5]):

        direcciones_totales = len(Direcciones[0])

        direcciones_descargadas = 0

        for email in Direcciones[0].values():

            Descargardor(email, 
                         Claves)

            direcciones_descargadas += 1

            if direcciones_descargadas % 2 == 0:
                
                clear()

                print(f"Progreso {round((direcciones_descargadas/direcciones_totales)*100,2)}%")
        
        print(Mensajes[7])

    else:

        print(f"\n\t{Mensajes[5]}\n\tActualice el archivo de direcciones validas")

    

    



