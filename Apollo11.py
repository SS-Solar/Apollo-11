import traceback
import random
from tqdm import tqdm
import time
from typing import NoReturn
import argparse

# Importación de Clases y métodos
from Archivos.Configuracion.Configuracion import Configuracion
#import Archivos.Configuracion.Configuracion as Configuracion
#import Archivos.Interfaz_Usuario.Interfaces as Menu
#import Archivos.Procesador.Generador as Procesador
#import Archivos.Procesador.Copia as Copia
from Archivos.Configuracion.Logger import Logger
from Archivos.InterfazUsuario.Interfaces import Interfaces
from Archivos.Procesador.Generador import Generador

# configuración del logger
logger = Logger
config = Configuracion()
menu = Interfaces()
procesador = Generador()


def main() -> NoReturn:
    
    try:
        parser = argparse.ArgumentParser(description='INGRESE LA OPCION QUE DESEA MODIFICAR.')
        parser.add_argument('--ciclo', type=float, help='Ciclo de tiempo en segundos')
        parser.add_argument('--min', type=float, help='Cambiar cantidad mínima de archivos a generar')
        parser.add_argument('--max', type=float, help='Cambiar cantidad máxima de archivos a generar')
        args = parser.parse_args()
        if args.ciclo is not None:
            config.cambiar_ciclo(args.ciclo)
            print('ciclo cambiado')
        elif args.min is not None:
            config.cambiar_min_archivos(args.min)
        elif args.max is not None:
            config.cambiar_max_archivos(args.max)
        else:
            print("No se suministraron opciones")
        # Configurar y obtener parámetros
        menu.menu_inicial()

        # Distribuir y ejecutar el proceso seleccionado
        while True:
            ciclo: float = config.ciclo()
            contador: int = 0
            lim_sup: int = config.cantidad_max_archivos()
            lim_inf: int = config.cantidad_min_archivos()
            cantidad_archivos: int = random.randint(lim_inf, lim_sup)
            print("Archivos de esta iteración: ", cantidad_archivos)
            logger.info("Archivos de esta iteración: %d", cantidad_archivos)
            barra: any = tqdm(total = cantidad_archivos, desc = "Procesando archivos:")
            for _ in range(cantidad_archivos):
                procesador.generar_archivos()
                barra.update(1)
                time.sleep(0.05)
            barra.close()
            contador = contador + 1
            logger.info("Iteracion " + str(contador) + "Completada.")
            print("Si desea Terminar de tomar datos, presionar CTRL+C y se generara el reporte")
            time.sleep(ciclo)
    except KeyboardInterrupt:
        procesador.generar_reportes()
        menu.mostrar_reporte()
        procesador.copiar_archivos_logs()
        print("Programa terminado. Saliendo...")
        logger.info("Programa terminado. Saliendo...")
    except Exception as e:
        logger.error("Ocurrió un error: %s", e)
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
