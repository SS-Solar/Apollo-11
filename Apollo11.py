import traceback
import random
from tqdm import tqdm
import time
from typing import NoReturn

# Importación de Clases y métodos
from Archivos.Configuracion.Configuracion import Configuracion
#import Archivos.Configuracion.Configuracion as Configuracion
import Archivos.Interfaz_Usuario.Interfaces as Menu
import Archivos.Procesador.Generador as Procesador
import Archivos.Procesador.Copia as Copia
from Archivos.Configuracion.Logger import Logger

# Configuración del logger
logger = Logger
Config = Configuracion()

def main() -> NoReturn:
    try:
        # Configurar y obtener parámetros
        Menu.menu_inicial()

        # Distribuir y ejecutar el proceso seleccionado
        while True:
            ciclo: float = Config.ciclo()
            contador: int = 0
            lim_sup: int = Config.cantidad_max_archivos()
            lim_inf: int = Config.cantidad_min_archivos()
            cantidad_archivos: int = random.randint(lim_inf, lim_sup)
            print("Archivos de esta iteración: ", cantidad_archivos)
            logger.info("Archivos de esta iteración: %d", cantidad_archivos)
            barra: any = tqdm(total = cantidad_archivos, desc = "Procesando archivos:")
            for _ in range(cantidad_archivos):
                Procesador.generar_archivos()
                barra.update(1)
                time.sleep(0.05)
            barra.close()
            contador = contador + 1
            logger.info("Iteracion " + str(contador) + "Completada.")
            print("Si desea Terminar de tomar datos, presionar CTRL+C y se generara el reporte")
            time.sleep(ciclo)
    except KeyboardInterrupt:
        Procesador.generar_reportes()
        Menu.mostrar_reporte()
        Copia.copiar_archivos_logs()
        print("Programa terminado. Saliendo...")
        logger.info("Programa terminado. Saliendo...")
    except Exception as e:
        logger.error("Ocurrió un error: %s", e)
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
