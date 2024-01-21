# librerías y dependencias Usadas
import yaml
import os
import platform
import traceback
import random
import typing
import logging
from tqdm import tqdm
import time

# importa la clase que contiene la lógica que se necesita
# from utilidades import Bootcamp
import Archivos.Configuracion.Configuracion as Config
import Archivos.Interfaz_Usuario.Interfaces as Menu
import Archivos.Procesador.Generador as Procesador

        
if __name__ == "__main__":

    try:
            # TODO 0.configurar y obtener parametros
        Menu.menu_inicial()
        # TODO 1.distribuir y ejecutar el proceso seleccionado
        while True:
            contador = 0
            cantidad_archivos = random.randint(Config.cantidad_min_archivos(),Config.cantidad_max_archivos())
            print("Cantidad de archivos de esta iteración: ", cantidad_archivos)
            barra = tqdm(total=cantidad_archivos, desc="Procesando archivos:")
            for i in range(cantidad_archivos): 
                Procesador.generar_archivos()
                barra.update(1)
                time.sleep(0.05)
            barra.close()
            print("Iteracion Completada.")
            print("Si desea Terminar de tomar datos, presionar CTRL+C y se generara el reporte")
            time.sleep(Config.ciclo())
    except KeyboardInterrupt:
        # Captura la excepción de interrupción del teclado (Ctrl+C)
        Procesador.generar_reportes()
        Menu.mostrar_reporte()

        print("Programa cancelado. Saliendo...")
    except Exception as e:
    #         # TODO 2.controlar errores globales de la app
    #         # manejo de excepción
            print("Ocurrió un error:", e)
            print(traceback.format_exc())