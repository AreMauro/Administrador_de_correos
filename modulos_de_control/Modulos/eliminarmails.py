import imaplib
from cuentaCorreo import cuentaDeCorreo
from Email import Email


import email

from DatosConexion import (
                                Carga_de_Datos)

from emaildresses import (
                Obtener_correos_spam, 
                Eliminar_Archivos_Temporales)

from pathlib import Path

from json import load

from Utilerias import (
                        Mensajes, 
                        clear)

from pprint import pprint

Raiz = Path("C:\\Users\\Ivan\\Downloads\\Desktop\\Proyectos\\modulos_de_control\\Administrador de mails\\Modulos")


def EliminarMailsporFechaycorreo(correo: str,
                                fecha: str,
                                nuevaCuenta: cuentaDeCorreo) -> None:
    
    emails = nuevaCuenta.getEmailsByDateAndAddress(correo, fecha)

    emailsHallados = len(emails)

    print(f"Se hallaron {emailsHallados} mails.")

    mailsEliminados = 0

    for email in emails:
        
        emailActual = Email(nuevaCuenta, email)

        nombre = emailActual.getSender()

        print(nombre)

        if nombre == correo:

            print("Eliminando...")

            emailActual.EliminarEmail()

        mailsEliminados += 1

        if mailsEliminados % 10 == 0:

            print(f"{round(mailsEliminados/emailsHallados, 4)*100}% completado")


def EliminarMailsporcorreo(correo: str,
                           nuevaCuenta: cuentaDeCorreo) -> None:

    emails = nuevaCuenta.getEmailsByAddress(correo)

    mailsEliminados = 0

    emailsHallados = len(emails)

    print(f"Se hallaron {emailsHallados} mails.")

    for email in emails:

        correoActual = Email(nuevaCuenta, email)

        nombre = correoActual.getSender()

        print(nombre)

        if nombre is not None:

            if nombre == correo:
                print("Aqui")
                correoActual.EliminarEmail()
            
            mailsEliminados += 1

            if mailsEliminados % 10 == 0:

                print(f"{round(mailsEliminados/emailsHallados, 4)*100}% completado")



def Eliminar_Todos_los_emails(cuenta: cuentaDeCorreo) -> None:

    Direcciones = Obtener_correos_spam(cuenta)

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
            
            print(email)

            EliminarMailsporcorreo(email, cuenta)

            direcciones_eliminadas += 1
            
            email = next(Emails, "Vacio")
            
            if direcciones_eliminadas % 10 == 0:

                clear()

                print(f"Progreso {round((direcciones_eliminadas/direcciones)*100,2)}%")


        print("Eliminando archivos temporales")

        Eliminar_Archivos_Temporales(directorio)

        print("Operacion completada con exito!!!")

