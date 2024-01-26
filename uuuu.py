    
import json
from datetime import datetime
#import Archivos.Configuracion.Configuracion as Config
from Archivos.Configuracion.Configuracion import Configuracion
from Archivos.Procesador.Analisis import Analisis
import random
import os
import hashlib
from typing import List
from Archivos.Configuracion.Logger import Logger
from Archivos.Procesador.Copia import Copia
logger = Logger
config = Configuracion()

    
def generar_archivos() -> None:
    """Genera los archivos de cada misión, organizandolo en carpetas y dandole numeros consecutivos
    """

    hash_encoded: str = 200
    mision: List[str] = config.misiones()
    misionaux: List[str] = mision
    print(misionaux)
    num_mis: int = len(mision)-1
    aux: int = random.randint(0, num_mis)
    mision: str = mision[aux]
    dispositivo: List[str] = config.dispositivos_mision(aux)
    num_dis: int = len(dispositivo)-1
    dispositivo: List[str] = dispositivo[random.randint(0, num_dis)]
    estado: List[str] = config.estado()
    num_estado:int = len(estado)-1
    estado:List[str] = estado[random.randint(0, num_estado)]
    actual:str = str(datetime.now().strftime("%d%m%Y%H%M%S"))
    ruta_script: str = os.path.abspath(__file__)
    ruta_logs: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ruta_script))), "Archivos", "Logs")
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



generar_archivos()