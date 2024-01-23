import shutil
import os
from datetime import datetime
from typing import List
def copiar_archivos_logs() -> None:
    """Copia los archivos logs en otra carpeta
    """
    actual:str = str(datetime.now().strftime("%d%m%Y%H%M"))
    ruta_script: str = os.path.abspath(__file__)
    ruta_logs: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ruta_script))), "Archivos", "Logs")
    ruta_copia_logs: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ruta_script))), "Archivos", "Reportes","Backups","Logs"+actual)
    shutil.copytree(ruta_logs, ruta_copia_logs)
    if os.path.exists(ruta_copia_logs):
        print(f"La carpeta '{ruta_logs}' se encuentra en: {ruta_copia_logs}")
    else:
        print(f"No se encontró la carpeta '{ruta_copia_logs}' en el directorio de inicio.")
    carpetas: List[str] =["ColonyMoon", "GalaxyTwo", "OrbitOne", "UNKW", "VacMars"]
    for carpeta in carpetas:
        ruta_carpeta_a_limpiar: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ruta_script))), "Archivos", "Logs",carpeta)
        eliminar_archivos_en_carpeta(ruta_carpeta_a_limpiar)
        

def eliminar_archivos_en_carpeta(ruta_carpeta: str) -> None:
    """Elimina los archivos de las misiones dentro de las carpetas logs 

    Args:
        ruta_carpeta (str): Ruta relativa o absoluta de la carpeta
    """
    for nombre_archivo in os.listdir(ruta_carpeta):
        ruta_archivo: str = os.path.join(ruta_carpeta, nombre_archivo)
        if os.path.isfile(ruta_archivo):
            os.remove(ruta_archivo)
        elif os.path.isdir(ruta_archivo):
            eliminar_archivos_en_carpeta(ruta_archivo)




    


