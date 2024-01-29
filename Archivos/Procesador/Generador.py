import json
from datetime import datetime
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



class Generador(Copia, Analisis):
    
    @staticmethod
    def generar_hash() -> str:
        """Genera hash

        Returns:
            str: Retorna el hash code
        """
        try:
            date_encoded:str = str(datetime.now().strftime("%d%m%y%H%M%S"))
            hasher:str = hashlib.sha1()
            logger.info("Se ha generado un hash")
            return hasher.hexdigest(), date_encoded
        except Exception as e:
            logger.error("Se ha generado un error en la generacion del hash: %s" % e)


    @staticmethod
    def generar_archivos() -> None:
        """Genera los archivos de cada misión, organizandolo en carpetas y dandole numeros consecutivos
        """
        try:
            hash_encoded: str = Generador.generar_hash()
            mision: List[str] = config.misiones()
            misionaux: List[str] = mision
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
            try:
                for misiones in misionaux:
                    rutaaux = os.path.join(ruta_logs, misiones)
                    if not os.path.exists(rutaaux):
                        os.makedirs(rutaaux)
                    rutaaux = os.path.join(ruta_logs, misiones)
                    
                    if misiones == mision:
                        nombre_archivo_log: str = Generador.nombre_archivo_log(rutaaux, mision)
                    
                # if mision == "UNKW":
                #     ruta_logs: str = os.path.join(ruta_logs,"UNKW")
                    
                # elif mision == "ColonyMoon":
                #     ruta_logs: str = os.path.join(ruta_logs,"ColonyMoon")
                #     nombre_archivo_log: str = os.path.join("Archivos/Logs/ColonyMoon", f"APL-"+ mision +"-"+ Generador.cantidad_de_archivos_en_carpeta("Archivos/Logs/ColonyMoon") +".log")
                # elif mision == "GalaxyTwo":
                #     nombre_archivo_log: str = os.path.join("Archivos/Logs/GalaxyTwo", f"APL-"+ mision +"-"+ Generador.cantidad_de_archivos_en_carpeta("Archivos/Logs/GalaxyTwo") +".log")
                # elif mision == "OrbitOne":
                #     nombre_archivo_log: str = os.path.join("Archivos/Logs/OrbitOne", f"APL-"+ mision +"-"+ Generador.cantidad_de_archivos_en_carpeta("Archivos/Logs/OrbitOne") +".log")
                # elif mision == "VacMars":
                #     nombre_archivo_log: str = os.path.join("Archivos/Logs/VacMars", f"APL-"+ mision +"-"+ Generador.cantidad_de_archivos_en_carpeta("Archivos/Logs/VacMars") +".log")
            except Exception as e:
                Logger.error("Error, ya existe el archivo, debe esperar 1 min para generar uno nuevo")
                
            with open(nombre_archivo_log, "a") as archivo_log:
                json.dump(datos, archivo_log)
                archivo_log.write("\n")
            logger.info("Se ha generado archivos correctamente")
        except Exception as e:
            logger.error("Error en la generacion de archivos: ", e)

    @staticmethod
    def generar_reportes() -> None:

        """Generacion de reportes analizando los archivos que hay en las carpetas de logs, a 
        a su vez creado archivo de reportes con el fin de almacenar un resumen de los resultados
        """
        try:
            a_eventos: str = Generador.eventos()
            g_desconexiones: str= Generador.gestion_desconexiones()
            tabla, d_inoperables, per_inoperables = Generador.dispositivos_inoperables()
            cm,gt,ob,vm,unk = Generador.Porcentajes()
            hash, date = Generador.generar_hash()
            nombre_reporte: str = os.path.join("Archivos","Reportes", f"APLSTATS-{date}.log") 
            with open(nombre_reporte, "a") as reporte:
                reporte.write(f"ANALISIS DE EVENTOS:\nLa informacion registrada a continuacion, muestra la cantidad de eventos por estado para cada dispositivo y mision\n{a_eventos}"'\n''\n'
                            f"GESTION DE DESCONEXIONES:\nRepresenta los dispositivos con un mayor numero de desconexiones\n{g_desconexiones}"'\n''\n'
                            f"Una vez analizadas todas las misiones de Apollo-11 se determina que hay {d_inoperables} dispositivos inoperables,\nlo que corresponde al {per_inoperables}% de todos los dispositivos existentes"'\n''\n'
                            f"DISPOSITIVOS INOPERABLES:\n{tabla}"'\n''\n'
                            f"La informacion resgitrada a continuacion contiene el porcentaje datos generados para cada dispositivo y misión con respecto a la cantidad total de datos.\n\n"
                            f"COLONYMOON:\n\n{cm}\n\n"
                            f"GALAXYTWO:\n\n{gt}\n\n"
                            f"ORBITONE:\n\n{ob}\n\n"
                            f"UNKNOW:\n\n{unk}\n\n")
            print(f"Estadisticas registrados en {nombre_reporte}")
            logger.info("Estadisticas registradas en: ", nombre_reporte)
        except Exception as e:
            logger.error("Error en la generacion de reportes: ", e)


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


    def nombre_archivo_log(ruta_logs: str, mision: str) -> str:
        """Genera nombre de un archivo log y lo almacena en su respectiva carpeta

        Args:
            ruta_logs (str): url de la ruta
            mision (str): mision la cual va a pertenecer el nombre

        Returns:
            str: _description_
        """
        nombre_archivo_log: str = os.path.join(ruta_logs, f"APL-"+ mision +"-"+ Generador.cantidad_de_archivos_en_carpeta(ruta_logs) +".log")
        return nombre_archivo_log