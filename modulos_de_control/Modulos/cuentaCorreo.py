import re
import imaplib
from pathlib import Path
from json import load, JSONDecodeError, dump
from emailConection import emailConection
from Utilerias import Mensajes
from pprint import pprint
from Email import Email
from traceback import print_exc
from shutil import rmtree
from tempfile import mkdtemp, NamedTemporaryFile
from Utilerias import clear

class cuentaDeCorreo:

    def __init__(self, correoElectronico: str,
                    nombreDeUsuario:str,
                    password:str,
                    proveedor:str ="gmail" ,
                    puerto: int =993,
                    puerto_ssl:int=465,
                    smtp: str='smtp.gmail.com'):

        self._correo = correoElectronico

        self._password = password
        
        self._usuario = nombreDeUsuario
        
        
        if any(char.isspace() for char in proveedor) == False and len(proveedor) >= 5:
            self._proveedor = proveedor

        else:
            raise Exception("Error el proveedor no debe contener espacios y debe tener al menos 5 caracteres de longitud")

        if isinstance(puerto, int) == True:
            self._puerto = puerto

        else:
            raise Exception("El puerto debe ser un entero.")

        if isinstance( puerto_ssl, int) == True:
            self._puerto_ssl = puerto_ssl

        else:
            raise Exception("El puerto debe ser un entero.")


        #CREAR UNA FUNCION QUE VALIDE ESTA PARTE USANDO REGEX
        if any(char.isspace() for char in smtp) == False:
            self._smtp = smtp

        else:
            raise Exception("Error el smtp es incorrecto")
        
        
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

    
    @property
    def  puerto(self) -> int:

        return self._puerto
    
    
    @property
    def puerto_ssl(self) -> int:

        return self._puerto_ssl
    
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
    
    
    @usuario.setter
    def usuario(self, username) ->None:

        if any(char.isspace() for char in username) == False and len(username) >=  5:
            self._usuario = username

    @proveedor.setter
    def proveedor(self, Nuevoproveedor) ->None:

        if any(char.isspace() for char in Nuevoproveedor) == False and len(Nuevoproveedor) >= 5:
            self._proveedor = Nuevoproveedor
    


    @puerto.setter
    def puerto(self, nuevoPuerto) ->None:

        if isinstance(nuevoPuerto, int) == False:

            self._puerto = nuevoPuerto

    @puerto_ssl.setter
    def puerto_ssl(self, nuevoPuerto) -> None:

        self._puerto_ssl = nuevoPuerto
    
    @smtp.setter
    def smtp(self, nuevoSMTP) -> None:

        self._smtp = nuevoSMTP

    def getConection(self) :

        conexion = emailConection(self._correo, self._password,
                              self._puerto, self._smtp
                              ).getConection()

        return conexion 


    def getEmailsByAddress(self, correo) ->list:

        conexion = self.getConection()

        Status, mensajes = conexion.search(None, f'FROM {correo}')

        mensajes = [x for x in mensajes[0].split()]

        conexion.close()

        conexion.logout()

        return mensajes


    def getAllEmails(self) ->list:

        conexion = self.getConection()

        Status, mensajes = conexion.search(None, "ALL")

        mensajes = [x for x in mensajes[0].split()]

        conexion.close()

        conexion.logout()

        return mensajes

    def getEmailsByDateAndAddress(self, correo: str,
                                fecha: str) -> list:
        """
            OBTIENE LOS MAILS DE UNA DIRECCION DE CORREO ESPECIFICA Y DE UNA FECHA IGUAL O POSTERIOR A FECHA.

        """

        conexion = self.getConection()

        Status, mensajes = conexion.search(None, f'FROM {correo} SINCE {fecha}')

        mensajes = [x for x in mensajes[0].split()]

        conexion.close()

        conexion.logout()

        return mensajes

    def getEmailsBeforeDate(self, fecha: str) -> list:

        """
            OBTIENE SOLO LOS EMAILS ANTERIORES A UNA FECHA ESPECIFICA
        """

        conexion = self.getConection()

        Status, mensajes = conexion.search(None, f'BEFORE {fecha}')

        mensajes = [x for x in mensajes[0].split()]

        conexion.close()

        conexion.logout()

        return mensajes

    def getEmailsAfterDate(self, fecha: str) -> list:

        """
            OBTIENE SOLO LOS EMAILS POSTERIORES A UNA FECHA ESPECIFICA
            
        """

        conexion = self.getConection()

        Status, mensajes = conexion.search(None, f'SINCE {fecha}')

        mensajes = [x for x in mensajes[0].split()]

        conexion.close()

        conexion.logout()

        return mensajes

    def Eliminar_spam(self, proveedor) -> None:

        nuevaconexion = imaplib.IMAP4_SSL(self._smtp, self._puerto)

        nuevaconexion.login(self._correo, self._password)

        mails = nuevaconexion.select(f"[{proveedor}]/Spam")

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

    def CrearArchivosTemporales(self) -> tuple:

        """
            Crea los archivos temporales que se utilizan para almacenar las direcciones de correo que no son considerados como 

        """

        print("Creando...")

        DireccionesAlmacenadas = Path( 
                    ".\\Datos\\Direcciones de correo")

        CorreosValidos= Path(
                    ".\\Datos\\Direcciones de correo\\Direcciones Validas.json")


        if DireccionesAlmacenadas.exists() == False:

            DireccionesAlmacenadas.mkdir()

            CorreosValidos.touch()
    
        else:

            if CorreosValidos.is_file() == False:

                CorreosValidos.touch()

                return (CorreosValidos,)

    def Cargar_Datos(self, arch : Path) -> tuple:

        try:
        
            with open(arch, "r") as JsonFile:

                Datos_Antiguos = load(JsonFile)
        
            return (Datos_Antiguos, Mensajes[7])

        except JSONDecodeError:

            return ("", )

        except:

            return (Mensajes[5], )

    def Direccion_valida(self, correo: bytes) -> bool:

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

    

    def direcciones_existentes(self) -> dict:

        direcciones = Path( 
                    ".\\Datos\\Direcciones de correo\\Direcciones Validas.json")

        if direcciones.is_file() == True:

            patrones = self.Cargar_Datos(direcciones)
        
            if patrones[0] == "":

                return {}

            if patrones[1] == Mensajes[7]:

                return patrones[0]
    
        else:

            return {}

    def Clasificar_mails(self, correo: str
                     ) -> bool:

        Direcciones = self.direcciones_existentes()

        if len(Direcciones) == 0:

            return False
    
        else:

            for nombre in Direcciones.values():

                if correo == nombre == True:

                    return True
    
        return False

    def Clasificacion(self, Direcciones: set,
                  correos_validos: set) -> set:

        for email in Direcciones:

            invalides = self.Clasificar_mails(email)

            if invalides == True:

                continue;
                
            elif invalides == False:
                
                if email in correos_validos:

                    continue;

                valides = self.Direccion_valida(email)

            if valides == True:

                correos_validos.add(email)
            
        return correos_validos

    def Obtener_direcciones_validas(self) -> set:
    
        try:
            print("Obteniendo direcciones...")

            Direcciones = set()

            correos_validos = set()

            print("Conectando...")

            print("Buscando...")

            emails = self.getAllEmails()

            last_email_id = int(emails[-1]) + 1

            print(f"Se encontraron {last_email_id} mails")

            contadormails = 0

            for email in emails:

                emailActual = Email(self, email)

                nombre = emailActual.getSender()

                Direcciones.add(nombre)
        
                contadormails += 1
            
                print(contadormails)

                if contadormails % 200 == 0:
                
                    print("Clasificando...")

                    correos_validados = self.Clasificacion(Direcciones,
                                                  correos_validos)

                    Direcciones.clear()

                    clear()

                    print(f"Progreso: {round((contadormails/last_email_id)*100)}%...")

            print(Mensajes[7])

            print("Cerrando sesion...")

            pprint(correos_validados)

            return correos_validos
    
        except:
        
            print_exc()

            return [Mensajes[5]]


    def crear_dict(self, correos_validos: set, 
               inicio: int = 0) -> dict:

        Datos = list(correos_validos)

        dictDatos = {str(inicio + i) : Datos[i] 
                for i in range(len(Datos))}

        return dictDatos

    def Actualizar_Datos(self, correos_validos: dict) -> str:

        Base_de_datos = self.CrearArchivosTemporales()

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
        

    def Eliminar_Archivos_Temporales(self, 
                    Destino: Path) ->None:
    
        try:
        
            rmtree(Destino)

            return Mensajes[7]
    
        except FileNotFoundError:

            print ("El archivo no existe...")

            return Mensajes[7]
    
        except:

            return Mensajes[5]

    def Actualizar_direcciones_validas(self) -> None :

        DireccionesAlmacenadas = Path( 
                    ".\\Datos\\Direcciones de correo")

        self.Eliminar_Archivos_Temporales(DireccionesAlmacenadas)

        Datos = self.Obtener_direcciones_validas()

        pprint(Datos)

        nuevos_validos = self.crear_dict(Datos)

        pprint(nuevos_validos)

        Estado_actualizacion = self.Actualizar_Datos(nuevos_validos)

    
        if (Datos != Mensajes[6] and 
            Estado_actualizacion != Mensajes[7]):

            print(Mensajes[7])

        else:

            print(Mensajes[5])


    def Clasificacion2(self, Spam: Path,
                   Direcciones: set) -> str:

        CorreosValidos= Path(
                    ".\\Datos\\Direcciones de correo\\Direcciones Validas.json")

        if CorreosValidos.is_file() == False:
        
            self.Actualizar_direcciones_validas()


        Dictvalidos = self.Cargar_Datos(CorreosValidos)

        if Dictvalidos[0] != "":

            for email in Direcciones:
            
                if email not in Dictvalidos[0].values() and email is not None:

                    with open(Spam, "ab+") as sp:
                        
                        sp.write(bytes(email, "utf8"))

                        sp.write(b"\n")
                
            return Mensajes[7]
    
        else:

            return Mensajes[5]

    def Obtener_correos_spam(self) -> tuple:
        
        try:
            print("Obteniendo direcciones...")
            
            print("Creando archivos temporales...")

            Direcciones = set()

            Aqui = Path(".\\Datos\\")

            Dir = mkdtemp(dir=Aqui)

            Destino = Path(str(Dir))

            Spam = NamedTemporaryFile(
                    mode="ab+", dir=Destino, 
                    prefix="spam",
                    delete=False)

            emails = self.getAllEmails()

            last_email_id = int(emails[-1]) + 1

            print(f"Se encontraron {last_email_id} mails")

            contadormails = 0

            for email in emails:

                emailActual = Email(self, email)

                direccion = emailActual.getSender()

                Direcciones.add(direccion)

                contadormails += 1

                print(contadormails)
    
                if contadormails % 200 == 0:
                    
                    print("Clasificando...")

                    direcciones_Spam = Path(Spam.name)
                    
                    Estado = self.Clasificacion2(direcciones_Spam, 
                        Direcciones)

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

    
    def EliminarMailsporFechaycorreo(self, correo: str,
                                fecha: str) -> None:
    
        emails = self.getEmailsByDateAndAddress(correo, fecha)

        emailsHallados = len(emails)

        print(f"Se hallaron {emailsHallados} mails.")

        mailsEliminados = 0

        for email in emails:
            
            emailActual = Email(self, email)

            nombre = emailActual.getSender()

            print(nombre)

            if nombre == correo:

                print("Eliminando...")

                emailActual.EliminarEmail()

            mailsEliminados += 1

            if mailsEliminados % 10 == 0:

                clear()

                print(f"{round(mailsEliminados/emailsHallados, 4)*100}% completado")


    def EliminarMailsporcorreo(self, correo: str) -> None:

        emails = self.getEmailsByAddress(correo)

        mailsEliminados = 0

        emailsHallados = len(emails)

        print(f"Se hallaron {emailsHallados} mails.")

        for email in emails:

            correoActual = Email(self, email)

            nombre = correoActual.getSender()

            print(nombre)

            if nombre is not None:

                if nombre == correo:
                    print("Aqui")
                    correoActual.EliminarEmail()
                
                mailsEliminados += 1

                if mailsEliminados % 10 == 0:
                    clear()
                    print(f"{round(mailsEliminados/emailsHallados, 4)*100}% completado")



    def Eliminar_Todos_los_emails(self) -> None:

        Direcciones = self.Obtener_correos_spam()

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

                self.EliminarMailsporcorreo(email)

                direcciones_eliminadas += 1
                
                email = next(Emails, "Vacio")
                
                if direcciones_eliminadas % 10 == 0:

                    clear()

                    print(f"Progreso {round((direcciones_eliminadas/direcciones)*100,2)}%")


            print("Eliminando archivos temporales")

            self.Eliminar_Archivos_Temporales(directorio)

            print("Operacion completada con exito!!!")

    def enviarEmailConAtachments(self, ruta:str, Destinatario:str, subject: str) ->None:

        nuevoEmial = Email(self)

        nuevoEmial.Enviar_mail(Destinatario, subject, ruta)

    def DescargarAtachmentsByAddress(self, correo:str, ruta:str) -> bool:

        for email in self.getEmailsByAddress(correo):

            emailActual = Email(self, email)

            print(emailActual.getSender())

            resultado = emailActual.descargarContenido(ruta)

            return resultado

    def descargarAtachmentsByAddressAndSubject(self) -> None: pass




    def __str__(self):
        return f"Mi cuenta es {self._correo}, con usuario: {self._usuario} y proveedor: {self.proveedor}"

    def __repr__(self):

        cl = self.__class__.__name__

        return f"{cl}[usuario = {self._usuario}, correo = {self._correo}, proveedor = {self.proveedor}]"