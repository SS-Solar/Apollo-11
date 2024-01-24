import traceback
import random
from tqdm import tqdm
import time
import logging
from typing import NoReturn

# Importación de Clases y métodos
import Archivos.Configuracion.Configuracion as Config
import Archivos.Interfaz_Usuario.Interfaces as Menu
import Archivos.Procesador.Generador as Procesador
import Archivos.Procesador.Copia as Copia

# Configuración del logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main() -> NoReturn:
    try:
        # Configurar y obtener parámetros
        Menu.menu_inicial()

        # Distribuir y ejecutar el proceso seleccionado
        while True:
            contador: int = 0
            lim_sup: int = Config.cantidad_max_archivos()
            lim_inf: int = Config.cantidad_min_archivos()
            cantidad_archivos: int = random.randint(lim_inf, lim_sup)
            logging.info("Archivos de esta iteración: %d", cantidad_archivos)
            barra: any = tqdm(total=cantidad_archivos, desc="Procesando archivos:")
            
            for _ in range(cantidad_archivos):
                Procesador.generar_archivos()
                barra.update(1)
                time.sleep(0.05)
            barra.close()
            logging.info("Iteracion Completada.")
            logging.info("Si desea Terminar de tomar datos, presionar CTRL+C y se generara el reporte")
            time.sleep(Config.ciclo())
    except KeyboardInterrupt:
        Procesador.generar_reportes()
        Menu.mostrar_reporte()
        Copia.copiar_archivos_logs()
        logging.info("Programa cancelado. Saliendo...")
    except Exception as e:
        logging.error("Ocurrió un error: %s", e)
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    main()
