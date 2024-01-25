import json
from datetime import datetime
#import Archivos.Configuracion.Configuracion as Config
from Archivos.Configuracion.Configuracion import Configuracion
import random
import os
import hashlib
from typing import List
from Archivos.Configuracion.Logger import Logger

logger = Logger
Config = Configuracion()

@staticmethod
def generar_hash() -> str:
    """Genera hash

    Returns:
        str: Retorna el hash code
    """
    date_encoded:str = str(datetime.now().strftime("%d%m%y%H%M%S"))
    hasher:str = hashlib.sha1()
    return hasher.hexdigest(), date_encoded

@staticmethod
def generar_archivos() -> None:
    """Genera los archivos de cada misión, organizandolo en carpetas y dandole numeros consecutivos
    """
    try:
        hash_encoded: str = generar_hash()
        mision: str = Config.misiones()
        print(mision)
        num_mis: int = len(mision)-1
        aux: int = random.randint(0, num_mis)
        mision: List[str] = mision[aux]
        dispositivo: List[str] = Config.dispositivos_mision(aux)
        num_dis: int = len(dispositivo)-1
        dispositivo: List[str] = dispositivo[random.randint(0, num_dis)]
        estado: List[str] =Config.estado()
        num_estado:int = len(estado)-1
        estado:List[str] = estado[random.randint(0, num_estado)]
        actual:str = str(datetime.now().strftime("%d%m%Y%H%M%S"))
        if mision != "UNKW":
            datos: dict [str, str, str, str]= {
                "fecha": actual,
                "mision": mision,
                "device_type": dispositivo,
                "device_status": estado,
                "hash": hash_encoded
                    }
        else :
            datos: dict [str, str, str, str]= {
                "fecha": str(datetime.now()),  # Obtiene la fecha actual como un string
                "mision": "UNKW",
                "device_type": "unknown",
                "device_status": "unknown",
                "hash": "unknown"  # Tu hash específico aquí
                    }
        if mision == "UNKW":
            nombre_archivo_log: str = os.path.join("Archivos/Logs/UNKW", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/UNKW") +".log")
        elif mision == "ColonyMoon":
            nombre_archivo_log: str = os.path.join("Archivos/Logs/ColonyMoon", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/ColonyMoon") +".log")
        elif mision == "GalaxyTwo":
            nombre_archivo_log: str = os.path.join("Archivos/Logs/GalaxyTwo", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/GalaxyTwo") +".log")
        elif mision == "OrbitOne":
            nombre_archivo_log: str = os.path.join("Archivos/Logs/OrbitOne", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/OrbitOne") +".log")
        elif mision == "VacMars":
            nombre_archivo_log: str = os.path.join("Archivos/Logs/VacMars", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/VacMars") +".log")
        
        with open(nombre_archivo_log,"a") as archivo_log:
            json.dump(datos, archivo_log)
            archivo_log.write("\n")
        logger.info("Se ha generado archivos correctamente")
    except Exception as e:
        logger.error("Error en la generacion de archivos: ", e)

@staticmethod
def cantidad_de_archivos_en_carpeta(carpeta: str) -> str:
    """ Revisa la carpeta en especifico y a su vez retorna el numero de la cantidad de archivos que hay
    en dicha carpeta

    Args:
        carpeta (str): ruta relativa de la carpeta

    Returns:
        str: retorna el numero de la cantidad de archivos en la carpeta
    """
    try:
        archivos: str = os.listdir(carpeta)
        archivos: str = [archivo for archivo in archivos if os.path.isfile(os.path.join(carpeta, archivo))]
        return str(len(archivos))
    except FileNotFoundError:
        return str(0)
    
    
generar_archivos()