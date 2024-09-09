import imaplib

import email

from modulos_de_control.Modulos.DatosConexion import (
                                Carga_de_Datos)

from modulos_de_control.Modulos.emaildresses import (
                Obtener_correos_spam, 
                Eliminar_Archivos_Temporales)

from pathlib import Path

from json import load

from modulos_de_control.Modulos.Utilerias import (
                        Mensajes, 
                        clear)

from pprint import pprint

Raiz = Path("C:\\Users\\Ivan\\Downloads\\Desktop\\Proyectos\\modulos_de_control\\Administrador de mails\\Modulos")


def EliminarMailsporFechaycorreo(correo: str,
                                fecha: str,
                                Claves: dict) -> None:

    nuevaconexion = imaplib.IMAP4_SSL(Claves["proveedor"], int(Claves["puerto"]))

    nuevaconexion.login(Claves["username"], Claves["password"])
    
    mails = nuevaconexion.select("INBOX")

    Status, mensajes = nuevaconexion.search(None, f'FROM {correo} BEFORE {fecha}')

    mensajes = [x for x in mensajes[0].split()]

    MensajesHallados = len(mensajes)

    print(f"Se encontraron {MensajesHallados} mensajes")

    mailseliminados = 0

    porcentajeProgreso = 0

    for mail in mensajes:

        mailseliminados += 1

        nuevaconexion.store(mail,"+FLAGS", "\\Deleted")

        if mailseliminados % 2 == 0:
            
            porcentajeProgreso = (mailseliminados/MensajesHallados)*100

            print(f"Progreso: {porcentajeProgreso}%")

    nuevaconexion.expunge()

    nuevaconexion.close()

    nuevaconexion.logout()


def EliminarMailsporcorreo(correo: str,
                        Claves: dict) -> None:

    nuevaconexion = imaplib.IMAP4_SSL(Claves["proveedor"], int(Claves["puerto"]))

    nuevaconexion.login(Claves["username"], Claves["password"])
    
    mails = nuevaconexion.select("INBOX")

    Status, mensajes = nuevaconexion.search(None, f'FROM {correo}')

    mensajes = [x for x in mensajes[0].split()]

    MensajesHallados = len(mensajes)

    print(f"\n\nSe van a eliminar los correos del email {correo}\n\n")

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


def Eliminar_spam(Claves: dict) -> None:

    nuevaconexion = imaplib.IMAP4_SSL(Claves["proveedor"], int(Claves["puerto"]))

    nuevaconexion.login(Claves["username"], Claves["password"])

    mails = nuevaconexion.select("[Gmail]/Spam")

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


def Eliminar_Todos_los_emails(Claves: dict) -> None:

    Direcciones = Obtener_correos_spam()

    if Direcciones[0] != Mensajes[5]:

        print("Obteniendo direcciones spam...")

        spam = Path(Direcciones[0])

        directorio = Path("\\".join(str(spam.resolve()).split("\\")[:-1]))

        direcciones_basura = set(open(spam).readlines())

        direcciones = len(direcciones_basura)

        direcciones_eliminadas = 0

        print("Eliminando direcciones...")

        Emails = iter(direcciones_basura)

        email = next(Emails, "Vacio")

        while  email != "Vacio":
  
            EliminarMailsporcorreo(email.rstrip("\n"))

            direcciones_eliminadas += 1

            email = next(Emails, "Vacio")
            
            if direcciones_eliminadas % 10 == 0:

                clear()

                print(f"Progreso {round((direcciones_eliminadas/direcciones)*100,2)}%")

        Eliminar_spam()

        print("Eliminando archivos temporales")

        Eliminar_Archivos_Temporales(directorio)

        print("Operacion completada con exito!!!")

