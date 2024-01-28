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
    def bienvenido() -> None:
        print("Dentro de Interfaces.bienvenido()")
    mensaje: str = "Bienvenido A"
    arte: any = text2art(mensaje, font="")
    print(arte)

    @staticmethod
    def apollo11() -> None:
        print("Dentro de Interfaces.apollo11()")
    mensaje: str = "APOLLO-11"
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
    def menu_inicial() -> None:
        Config.ciclo()
        nombre = input(" ¿DESEA CONTINUAR CON LOS ANTERIORES DATOS? [y/n]: ")
        if nombre.lower() == "n":
            opcion = ""  """Inicializa opción como cadena vacía"""
        while opcion != "7":
            opcion = input("Que información desea cambiar?\n 1. Ciclo de tiempo (s)\n 2. Eliminar Dispositivos \n 3. Añadir un nuevo dispositivo \n 4. Cambiar cantidad mínima de archivos a generar \n 5. Cambiar cantidad máxima de archivos a generar \n 6. Crear copia del último reporte disponible \n 7. Seguir a la generación de archivos \n")
            if opcion == "1":
                ciclo = input("Ingrese nuevo ciclo de tiempo: ")
                try:
                    Config.cambiar_ciclo(float(ciclo))
                    logging.info(f"Ciclo cambiado a {ciclo}")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
                    logging.error("Entrada inválida para el ciclo.")
            elif opcion == "2":
                mision = input("Ingrese el nombre de la misión de la cual eliminar el dispositivo: ")
                dispositivo_a_eliminar = input("Ingrese el nombre del dispositivo a eliminar: ")
                Config.eliminar_dispositivo(mision, dispositivo_a_eliminar)
            elif opcion == "3":
                mision = input("Ingrese el nombre de la misión para la cual agregar nuevo dispositivo: ")
                nuevo_dispositivo = input("Ingrese el nombre del nuevo dispositivo: ")
                Config.nuevo_dispositivo(mision, nuevo_dispositivo)
            elif opcion == "4":
                cantidad_min_archivos:int = int(input ("Ingrese nueva cantidad minima de archivos a generar: "))
                Config.cambiar_min_archivos(cantidad_min_archivos)
            elif opcion == "5":
                cantidad_max_archivos:int = int(input ("Ingrese nueva cantidad máxima de archivos a generar: "))
                Config.cambiar_max_archivos(cantidad_max_archivos)
            elif opcion == "6":
                Config.Crear_copia()
                print("Copia creada con éxito")
                logging.info("Copia de reporte creada.")
            elif opcion == "7":
                print("Continuando con la generación de archivos...")
                logging.info("Continuando con la generación de archivos.")
            else:
                print("Opción errónea, inténtelo otra vez.")
                logging.warning("Opción errónea seleccionada en el menú.")
