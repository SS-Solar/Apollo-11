import logging
import os
from art import text2art
from typing import List 
#import Archivos.Configuracion.Configuracion as Config
from Archivos.Configuracion.Configuracion import Configuracion
import argparse

Config = Configuracion()


class Interfaces:


    @staticmethod
    def apollo11() -> None:
        """Muestra el codigo ASCII del mensaje Apollo 11
        """
        mensaje: str = "APOLLO-11"
        arte: any = text2art(mensaje, font="")
        print(arte)


    @staticmethod
    def bienvenido() -> None:
        """Muestra el codigo ASCII del mensaje Bienvenidos
        """
        mensaje: str = "Bienvenido A"
        arte: any = text2art(mensaje, font="")
        print(arte)


    @staticmethod
    def mostrar_reporte() -> None:
        """Muestra el último reporte generado."""
        carpeta = 'Archivos/Reportes/'
        try:
            archivos = os.listdir(carpeta)
            archivos = [archivo for archivo in archivos if os.path.isfile(os.path.join(carpeta, archivo))]
            archivos.sort(key=lambda x: os.path.getmtime(os.path.join(carpeta, x)))
            if archivos:
                ultimo_archivo = archivos[-1]
                with open(os.path.join(carpeta, ultimo_archivo), 'r') as file:
                    contenido:str = file.read()
                logging.info("Se ha mostrado el reporte correctamente en consola")
            else:
                logging.warning("La carpeta está vacía o no contiene archivos.")
            print(contenido)
        except Exception as e:
            logging.error("Error al mostrar el reporte", exc_info=True)

    @staticmethod
    def menu_inicial()-> None:
        Interfaces.bienvenido()
        Interfaces.apollo11()
        #Config.dispositivos()
        Config.ciclo()
        # Las siguientes operaciones se realizan en el módulo de configuración, se asume que están correctamente ajustadas con logging.
        nombre = input(" ¿DESEA CONTINUAR CON LOS ANTERIORES DATOS? [y/n]: ")
        if nombre.lower() == "n":
            opcion =0
            while ( not (opcion == 7)):
                opcion = input ("Que informacióm desea cambiar?\n 1. Ciclo de  tiempo (s)\n 2. Eliminar Dispositivos \n 3. Añadir un nuevo dispositivo \n 4. Cambiar cantidad minima de archivos a generar \n 5. Cambiar cantidad maxima de archivos a generar \n 6. Crear copia del ultimo reporte disponible \n 7. Seguir a la generacion de archivos \n" )
                if opcion == "1":
                    ciclo = input("Ingrese nuevo ciclo de tiempo: ")
                    Config.cambiar_ciclo(float(ciclo))
                    break
                elif opcion == "2":
                    Config.menu_eliminar_dispositivo()
                    break
                elif opcion == "3":
                    Config.menu_nuevo_dispositivo()
                    break
                elif opcion == "4":
                    Config.menu_cambiar_min_archivos()
                    break
                elif opcion == "5":
                    Config.menu_cambiar_max_archivos()
                    break
                elif opcion == "6":
                    Config.Crear_copia()
                    break
                elif opcion == "7":
                    break
                else:
                    print("Opción errónea, inténtelo otra vez.")
                    logging.info("Opción errónea, inténtelo otra vez.")

                    
