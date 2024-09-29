from os import system

Mensajes = {1 : "Dame la contraseña de la aplicacion gmail: ",
            2 : "Dame el correo electronico: ", 
            3 : "Y/N:", 
            4: "Este campo no puede dejarse vacio.",
            5: "Error Interno.",
            6: "La opcion no existe.",
            7: "Operacion exitosa.", 
            8: "Operacion abortada.",
            9: "Dame el Asunto del correo: ",
            10: """
                Elige una opcion.
                Oprime S para enviar Emails.
                Oprime E para eliminar Emails.
                Oprime D para descargar Emails.
                Oprime A para actualizar informacion.
                Escribe exit para salir.
                """,
            11: "Desea salir del programa?",
            12: """
                Elige una opcion
                Oprime T para eliminar todos los emails basura de la cuenta.
                Oprime P para eliminar todos los correos de una sola direccion.
                Oprime F para eliminar todos los correos de una sola direccion antes de una fecha especifica.
                """,
            13: "Dame la fecha en este formato: '01-Jan-2012'.",
            14: "Dame tu usuario:",
            15: "Usuario no registrado.",
            16: "Desea registrar al usuario?",
            17: "Escribe tu proveedor de email, solo: gmail o outlook:",
            18: "Vuelve pronto!!!",
            19: """
                Elija alguna de las siguientes opciones:
                D para descargar todos los mails de la lista de validos.
                C para descargar todos correos de una direccion valida.
                """,
            20: "Desea registrar al nuevo usuario.",
            21: """
                    Elija alguna de las siguientes opciones:
                    C para cambiar la contraseña del usuario.
                    D para cambiar la contraseña de la aplicacion.
                    P para cambiar el correo electronico.
                    F para cambiar el proveedor.
                    T para ver toda la informacion del usuario.
                """,

            }

clear = lambda : system("cls")

def Formato(Texto : str) -> str:

    Formato = "\n\t\t{Frase}\n\t\t"
    
    for separador in [":", "?", ".", "!!!", "..."]:
        
        if separador in Texto:

            resultado = "".join(
                [ Formato.format(
                Frase = Frase) 
                for Frase in Texto.split(separador)])

            return resultado

def Pedir_informacion(Informacion: str) -> str:

    try:
        correcto = False

        while correcto == False:
            
            texto_formateado = Formato(Informacion)

            correo = input(texto_formateado )

            if any(correo):

                return correo
            
            else: 
                
                print(Mensajes[4])
                
                correcto = False
    
    except KeyboardInterrupt:

        print(Mensajes[8])

        quit()


def Autorizacion(texto: str) -> str:

    try:

        print(Formato(texto))

        valido = False

        while valido == False:

            Answer = input(Formato(Mensajes[3]))
            
            if any(Answer) and ("Y" == Answer.upper() or
                                "N" == Answer.upper()):

                return Answer.upper()
            
            elif any(Answer) == False:

                print(Mensajes[4])

                valido = False
            
            else:

                print(Mensajes[6])

                valido = False

    except KeyboardInterrupt:

        print(Mensajes[8])

        quit()



