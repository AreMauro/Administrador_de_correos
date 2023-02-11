from modulos_de_control.Administrador import(
                            Administracion)

from modulos_de_control.Login import LogIn

from modulos_de_control.Modulos.Utilerias import(
                                    Autorizacion,
                                    Mensajes,
                                    clear)

from traceback import print_exc

def Aplicacion():

    try:

        continua = True

        while continua == True:

            clear()

            Claves = LogIn()    

            if Claves is not None:

                continua = Administracion(Claves)
            
            else:

                
                quit()

    except SystemExit:
        
        pass

    except:

        print_exc()
        pass

if __name__ == "__main__": 

    Aplicacion()

