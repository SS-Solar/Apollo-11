
import json
from datetime import datetime
import Archivos.Configuracion.Configuracion as Config
import random
import os
import hashlib


def generar_hash():
    """Genera hash

    Returns:
        str: Retorna el hash code
    """
    date_encoded:str = str(datetime.now().strftime("%d%m%y%H%M%S"))
    hasher:str = hashlib.sha1()
    #hasher.update(date_encoded.encode())
    return hasher.hexdigest(), date_encoded

#Datos a incluir en el archivo JSON
def generar_archivos():
    """Genera los archivos de cada misión, organizandolo en carpetas y dandole numeros consecutivos
    """
    hash_encoded = generar_hash()
    mision = Config.misiones()
    num_mis= len(mision)-1
    aux= random.randint(0, num_mis)
    mision = mision[aux]
    dispositivo= Config.dispositivos_mision(aux)
    num_dis = len(dispositivo)-1
    dispositivo = dispositivo[random.randint(0, num_dis)]
    estado= Config.estado()
    num_estado= len(estado)-1
    estado= estado[random.randint(0, num_estado)]
    #Toma de fecha y hora actual 
    actual= datetime.now()
    actual = str(actual.strftime("%d%m%Y%H%M%S"))
    if mision != "UNKW":
        datos = {
            "fecha": actual,
            "mision": mision,
            "device_type": dispositivo,
            "device_status": estado,
            "hash": hash_encoded
                }
    else :
        datos = {
            "fecha": str(datetime.now()),  # Obtiene la fecha actual como un string
            "mision": "UNKW",
            "device_type": "unknown",
            "device_status": "unknown",
            "hash": "unknown"  # Tu hash específico aquí
                }
    if mision == "UNKW":
        nombre_archivo_log = os.path.join("Archivos/Logs/UNKW", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/UNKW") +".log")
    elif mision == "ColonyMoon":
        nombre_archivo_log = os.path.join("Archivos/Logs/ColonyMoon", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/ColonyMoon") +".log")
    elif mision == "GalaxyTwo":
        nombre_archivo_log = os.path.join("Archivos/Logs/GalaxyTwo", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/GalaxyTwo") +".log")
    elif mision == "OrbitOne":
        nombre_archivo_log = os.path.join("Archivos/Logs/OrbitOne", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/OrbitOne") +".log")
    elif mision == "VacMars":
        nombre_archivo_log = os.path.join("Archivos/Logs/VacMars", f"APL-"+ mision +"-"+ cantidad_de_archivos_en_carpeta("Archivos/Logs/VacMars") +".log")
    
    with open(nombre_archivo_log,"a") as archivo_log:
        json.dump(datos, archivo_log)
        archivo_log.write("\n")
        
def generar_reportes():
    a_eventos = Config.Crear_DataFrame()
    #.to_string(index=False)
    g_desconexiones= Config.Gestion_Desconexiones()
    d_inoperables, per_inoperables = Config.Dispositivos_inoperables()
    porcentajes= Config.Porcentajes()
    hash, date = generar_hash()
    nombre_reporte= os.path.join("Archivos","Reportes", f"APLSTATS-{date}.log") 
    with open(nombre_reporte, "a") as reporte:
        reporte.write(f"ANALISIS DE EVENTOS:\nLa informacion registrada a continuacion, muestra la cantidad de eventos por estado para cada dispositivo y mision\n{a_eventos.to_string(index=False)}"'\n''\n'
                    f"GESTION DE DESCONEXIONES:\nRepresenta los dispositivos con un mayor numero de desconexiones\n{g_desconexiones.to_string(index=False)}"'\n''\n'
                    f"Una vez analizadas todas las misiones de Apollo-11 se determina que hay {d_inoperables} dispositivos inoperables,\nlo que corresponde al {per_inoperables}% de todos los dispositivos existentes"'\n''\n'
                    f"TABLA DE PORCENTAJES\n{porcentajes.to_string(index=False)}")
    print(f"Estadisticas registrados en {nombre_reporte}")

def cantidad_de_archivos_en_carpeta(carpeta):
    try:
        archivos = os.listdir(carpeta)
        archivos = [archivo for archivo in archivos if os.path.isfile(os.path.join(carpeta, archivo))]
        return str(len(archivos))
    except FileNotFoundError:

        return str(0)

