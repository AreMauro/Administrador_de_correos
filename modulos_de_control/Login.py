from modulos_de_control.Modulos.Utilerias import (
                                Pedir_informacion,   
                                Autorizacion,
                                Mensajes,
                                clear,
                                Formato)

from modulos_de_control.Modulos.baseDeDatos import Datos

from traceback import print_exc

from sys import exit

from modulos_de_control.Modulos.Usuario import Usuario

from modulos_de_control.Modulos.cuentaCorreo import cuentaDeCorreo


def registrarNuevoUsuario() -> None:

    BasedeDatos = Datos()

    informacion_valida = False

    usuario = Pedir_informacion("Escriba su username.")

    while informacion_valida == False:

        #clear()

        Pasword = Pedir_informacion("Escriba su contraseña.")

        if(Usuario._verificadordeContrasegna(Pasword) ==  False):

            print(Formato("Contraseña no valida."))

            informacion_valida = False

        else:

            informacion_valida = True
    
    
    BasedeDatos.insertIntoUsuario(usuario, Pasword)

    informacion_valida = False

    while informacion_valida == False:

        #clear()

        Correo = Pedir_informacion("Dame el correo electronico::")

        if(cuentaDeCorreo._verificarCorreo(correo=Correo) ==  False):

            print(Formato("Correo no valido."))

            informacion_valida = False

        else:

            informacion_valida = True
    
        
    password_de_la_cuenta = Pedir_informacion("Dame el Password de la cuenta de correo (password de aplicacion de google)::")
        
    proveedor = Pedir_informacion("Dame el proveedor.")

    BasedeDatos.insertIntoCuentadeCorreo(usuario, Correo, password_de_la_cuenta, proveedor)


def LogIn() -> tuple:

    try:
        valido = False

        BaseDeDatos = Datos()

        while valido == False:

            #clear()
            
            Usuario = Pedir_informacion(Mensajes[14])

            usuarioActual = BaseDeDatos.getUsuario(Usuario)

            if (usuarioActual is None):
                
                #clear()

                print(Formato("El usuario no existe."))

                registro = Autorizacion(Mensajes[20])

                if registro == "Y":

                    #clear()

                    registrarNuevoUsuario()
                    
                    valido =  False
                
                else:
                    
                    salida = Autorizacion(Mensajes[11])

                    if salida == "Y":

                        quit()
                    
                    else:

                        valido = False
            elif(usuarioActual is not None):

                print(Formato("Usuario registrado."))
                
                password = Pedir_informacion("Dame la contraseña.")

                if(password == usuarioActual.password):

                    cuentaActual = BaseDeDatos.getCuenta(usuarioActual.username[0])

                    return (usuarioActual, cuentaActual)
                else:
                    print("Contraseña invalida")
                    valido = False


    except SystemExit:
        
        pass

    except KeyboardInterrupt:

        print(Mensajes[8])

        quit()


    except:

        print_exc()

        return Mensajes[5]

       

