import logging
import os
from art import text2art
from typing import List 
from Archivos.Configuracion.Configuracion import Configuracion
import argparse
from Archivos.Configuracion.Logger import Logger

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
                Logger.info("Se ha mostrado el reporte correctamente en consola")
            else:
                Logger.warning("La carpeta está vacía o no contiene archivos.")
            print(contenido)
        except Exception as e:
            Logger.error("Error al mostrar el reporte", exc_info=True)

    @staticmethod
    def menu_inicial() -> None:
        try:
            Interfaces.bienvenido()
            Interfaces.apollo11()
            Config.dispositivos()
            Config.ciclo()
            nombre= input (" ¿DESEA CONTINUAR CON LOS ANTERIORES DATOS? [y/n]: ")
            if (nombre == "n"):
                    opcion = 0
                    while ( not (opcion == 6)):
                        opcion = input ("Que informacióm desea cambiar?\n 1. Ciclo de  tiempo (s)\n 2. Eliminar Dispositivos \n 3. Añadir un nuevo dispositivo \n 4. Cambiar cantidad minima de archivos a generar \n 5. Cambiar cantidad maxima de archivos a generar \n 6. Seguir con la generacion de archivos\n" )
                        if opcion=="1":
                            ciclo:int = input("Ingrese nuevo ciclo de tiempo: ")
                            Config.cambiar_ciclo(float(ciclo))
                        elif opcion=="2":
                            misiones = Config.misiones()
                            print("A que mision desea eliminar un dispositivo?")
                            for i,y in enumerate(misiones):
                                print(f"{i+1}. {y}")
                            mision:int = int(input ("Ingrese opcion de misión de donde desea eliminar el dispositivo: "))
                            
                            dispositivos = Config.dispositivos_mision(mision-1)
                            print("¿Cuál dispositivo desea eliminar?")
                            for j,k in enumerate(dispositivos):
                                print(f"{j+1}. {k}")
                            dispositivo:int = int(input("Ingrese opcion del dispositivo que desea eliminar: "))
                            Config.eliminar_dispositivo(misiones[mision-1],dispositivo-1)
                            #Config.cambiar_ciclo(float(ciclo))
                            #Eliminar dispositvo de mision especifica
                        elif opcion=="3":
                            #mision = int(input ("A que mision dese añadir un dispositivo?\n 1. ColonyMoon \n 2. GalaxyTwo \n 3. OrbitOne \n 4. VacMars\n"))
                            misiones = Config.misiones()
                            print("A que mision desea añadir un dispositivo?")
                            for i,y in enumerate(misiones):
                                print(f"{i+1}. {y}")
                            mision = int(input("(ingrese un número de opción): "))
                            dispositivo = input (" Ingrese el nombre del nuevo dispositivo:  ")
                            #mision_aux = Config.misiones() 
                            mision = misiones[mision-1]
                            Config.nuevo_dispositivo (mision,dispositivo)
                        elif opcion=="4":
                            cantidad_min_archivos:int = int(input ("Ingrese nueva cantidad minima de archivos a generar: "))
                            Config.cambiar_min_archivos(cantidad_min_archivos)
                        elif opcion=="5":
                            cantidad_max_archivos:int = int(input ("Ingrese nueva cantidad maxima de archivos a generar: "))
                            Config.cambiar_max_archivos(cantidad_max_archivos)
                        elif opcion=="6":
                            break
                        else: 
                            print("Opcion erronea, intentalo otra vez")
            Logger.info("Se desplego correctamente el menu")
        except Exception as e:
            Logger.error("Error en mostrar el menu")