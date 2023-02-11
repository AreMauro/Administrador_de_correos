from modulos_de_control.Modulos.Utilerias import (
                                Pedir_informacion,   
                                Autorizacion,
                                Mensajes,
                                clear,
                                Formato)

from modulos_de_control.Modulos.DatosConexion import (
                            Carga_de_Datos)

from traceback import print_exc

from sys import exit

def LogIn() -> str:

    try:
        valido = False

        while valido == False:
            #clear()
            Usuario = Pedir_informacion(Mensajes[14])

            Credenciales = Carga_de_Datos(Usuario)

            if (1 in Credenciales.keys() and
                "" in Credenciales.values()):

                Salida = Autorizacion(Mensajes[11])

                if Salida == "Y":

                    exit()
                
                else:

                    valido = False
            
            
            elif (1 in Credenciales.keys() and
                 Mensajes[7] in Credenciales.values()):

                clear()

                print(Mensajes[7])

                print(Formato("Reingresando..."))

                valido = False
            
            else:

                return Credenciales

    except SystemExit:
        
        pass

    except KeyboardInterrupt:

        print(Mensajes[8])

        quit()


    except:

        print_exc()

        return Mensajes[5]

        

