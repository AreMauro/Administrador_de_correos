from imbox import Imbox

import os

from pathlib import Path

from modulos_de_control.Modulos.DatosConexion import (
                                Carga_de_Datos)

from modulos_de_control.Modulos.emaildresses import (
                            Cargar_Datos)

from pathlib import Path

from modulos_de_control.Modulos.Utilerias import (
                                clear, 
                                Mensajes)

from pprint import pprint

def Archivos_directorio(directorio: Path):

    return [ el.name 
            for el 
            in list(directorio.iterdir())]

def Cambiar_nombre(name_file : str,
                    directorio : Path) -> str:

    Existe = True

    archivos = Archivos_directorio(directorio)

    contador = 0

    while Existe:

        if name_file not in archivos:

            return name_file

        else:
            
            punto = name_file.find(".")

            nombre_archivo = name_file [:punto]

            nombre_archivo += f"({contador})"

            nombre_archivo += name_file [punto :]

            if nombre_archivo in archivos:

                    contador += 1

                    Existe = True
            
            else:

                return nombre_archivo


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

    

    



