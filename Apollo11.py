# librerías y dependencias Usadas
import traceback
import random
from tqdm import tqdm
import time
# Importacion de Clases y metodos
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
            lim_sup: int = Config.cantidad_max_archivos()
            lim_inf: int = Config.cantidad_min_archivos()
            cantidad_archivos: int = random.randint(lim_inf, lim_sup)
            print("Archivos de esta iteración: ", cantidad_archivos)
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
        Procesador.generar_reportes()
        Menu.mostrar_reporte()
        print("Programa cancelado. Saliendo...")
    except Exception as e:
        print("Ocurrió un error:", e)
        print(traceback.format_exc())
