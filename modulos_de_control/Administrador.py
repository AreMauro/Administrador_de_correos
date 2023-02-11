from modulos_de_control.Modulos.EnviarEmails import (
                                Enviar_mail)

from modulos_de_control.Modulos.Utilerias import (
                    Pedir_informacion,
                    Mensajes, 
                    Autorizacion,
                    clear,
                    Formato)

from modulos_de_control.Modulos.eliminarmails import ( 
                    EliminarMailsporFechaycorreo,
                    EliminarMailsporcorreo,
                    Eliminar_Todos_los_emails)

from modulos_de_control.Modulos.DescargaMails import(
                    Descargardor,
                    Descargar_de_direcciones_validas
)

from traceback import print_exc

def Administracion(claves: dict):

    try:

        Salida = "N"

        while Salida == "N":

            clear()

            Peticion = Pedir_informacion(Mensajes[10])

            if Peticion.upper() == "S":

                Asunto = Pedir_informacion(Mensajes[9])

                Correo_destino = Pedir_informacion(Mensajes[2])

                Enviar_mail(Correo_destino,
                            Asunto,
                            claves)
                
                Salida = Autorizacion(Mensajes[11])

                if Salida == "Y":
                    clear()
                    quit()

            elif Peticion.upper() == "E":

                clear()

                Subopcion = Pedir_informacion(Mensajes[12])

                if Subopcion.upper() == "T":

                    Eliminar_Todos_los_emails(claves)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                    
                        quit()
                
                elif Subopcion.upper() == "P":

                    Correo = Pedir_informacion(Mensajes[2])

                    EliminarMailsporcorreo(Correo,
                                        claves)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                    
                        quit()
                
                elif Subopcion.upper() == "F":
                    
                    Correo = Pedir_informacion(Mensajes[2])

                    Fecha = Pedir_informacion(Mensajes[13])

                    EliminarMailsporFechaycorreo(Correo,
                    Fecha,
                    claves)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                    
                        quit()

            elif Peticion.upper() == "D":

                clear()
                
                Subopcion = Pedir_informacion(Mensajes[19])
                
                clear()

                if Subopcion.upper() == "C":

                    Correo = Pedir_informacion(Mensajes[2])

                    Descargardor(Correo,
                                claves)

                    Salida = Autorizacion(Mensajes[11])

                    if Salida == "Y":
                        
                        quit()
                elif Subopcion.upper() == "D":

                    pass

            elif Peticion.upper() == "C":
                
                clear()
                return True


            elif Peticion.upper() == "EXIT":

                clear()
                quit()
            
            elif Peticion.upper() == "A":

                clear()
                quit()

    except SystemExit:

        #clear()

        print(Formato(Mensajes[18]))

    except KeyboardInterrupt:

        print(Formato(Mensajes[8]))

        quit()


    except:

        print_exc()


