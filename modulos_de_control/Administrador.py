from modulos_de_control.Modulos.Utilerias import (
                    Pedir_informacion,
                    Mensajes, 
                    Autorizacion,
                    clear,
                    Formato)
from modulos_de_control.Modulos.baseDeDatos import Datos

from modulos_de_control.Modulos.Usuario import Usuario

from modulos_de_control.Modulos.cuentaCorreo import cuentaDeCorreo

from pprint import pprint

from traceback import print_exc

def Administracion(claves: tuple[Usuario, cuentaDeCorreo ]) -> None:

    try:

        Salida = "N"

        while Salida == "N":

            clear()

            Peticion = Pedir_informacion(Mensajes[10])

            if Peticion.upper() == "S":

                Asunto = Pedir_informacion(Mensajes[9])

                Correo_destino = Pedir_informacion(Mensajes[2])

                ruta = Pedir_informacion("Dame la direccion donde estan los archivos.")

                claves[1].enviarEmailConAtachments(ruta, Correo_destino, Asunto)

                Salida = Autorizacion(Mensajes[11])

                if Salida == "Y":
                    clear()
                    quit()

            elif Peticion.upper() == "E":

                clear()

                Subopcion = Pedir_informacion(Mensajes[12])

                if Subopcion.upper() == "T":
 
                    try:

                        claves[1].Eliminar_Todos_los_emails()
                    
                    except TimeoutError:

                        print("Error de conexion")

                    

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                    
                        quit()
                
                elif Subopcion.upper() == "P":

                    Correo = Pedir_informacion(Mensajes[2])

                    claves[1].EliminarMailsporcorreo(Correo)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                    
                        quit()
                
                elif Subopcion.upper() == "F":
                    
                    Correo = Pedir_informacion(Mensajes[2])

                    Fecha = Pedir_informacion(Mensajes[13])

                    claves[1].EliminarMailsporFechaycorreo(Correo,
                    Fecha)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                    
                        quit()

            elif Peticion.upper() == "A":

                basseDeDatos = Datos()
                clear()
                
                Subopcion = Pedir_informacion(Mensajes[21])
                
                clear()

                if Subopcion.upper() == "C":

                    passworNueva = Pedir_informacion("Dame la nueva contraseña.")

                    if(Usuario._verificadordeContrasegna(passworNueva)):

                        basseDeDatos.cambiarContraseña(claves[0].username [0], passworNueva)

                        Salida = Autorizacion(Mensajes[11])

                        if Salida == "Y":
                        
                            quit()
                elif Subopcion.upper() == "D":

                    passworNueva = Pedir_informacion("Dame la nueva contraseña de la aplicacion.")

                    basseDeDatos.cambiarContraseñaCuenta(claves[0].username[0], passworNueva)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                        
                        quit()  
                
                elif Subopcion.upper() == "P":

                    correoNuevo = Pedir_informacion("Dame la nueva contraseña.")

                    basseDeDatos.modificarCorreo(claves[0].username[0], correoNuevo)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                        
                        quit()
                
                elif Subopcion.upper() == "F":

                    proveedorNuevo = Pedir_informacion("Dame la nueva contraseña.")

                    basseDeDatos.modificarProveedor(claves[0].username[0], proveedorNuevo)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                        
                        quit()
                
                elif Subopcion.upper() == "T":

                    Informacion = basseDeDatos.getAllUserData(claves[0].username[0])

                    pprint(Informacion)
                    
                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                        
                        quit()

            elif Peticion.upper() == "EXIT":

                clear()
                quit()
            
            elif Peticion.upper() == "D":
                clear()
                
                Subopcion = Pedir_informacion(Mensajes[19])
                
                clear()

                if Subopcion.upper() == "C":

                    correo = Pedir_informacion("Dame el correo.")

                    ruta = Pedir_informacion("Da la ruta donde deseas guardar los archivos, usa el formato \\\\.")

                    claves[1].DescargarAtachmentsByAddress(correo, ruta)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                        
                        quit()
            
                elif Subopcion.upper() == "D":

                    pass


    except SystemExit:

        #clear()

        print(Formato(Mensajes[18]))

        quit()

    except KeyboardInterrupt:

        print(Formato(Mensajes[8]))

        quit()


    except:

        print_exc()


