# Dependencias
import yaml
import os
from typing import List
from Archivos.Configuracion.Logger import Logger

# Variables locales usadas

misiones_ar = List[str]
dispositivos_ar = List[str]
ruta_absoluta = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(ruta_absoluta, 'config.yaml')

# Apertura de archivo de configuracion para su respectivo uso

with open(ruta, "r") as file:
    data = yaml.safe_load(file)

logger = Logger

class Configuracion:


    @staticmethod
    def misiones() -> List[str]:
        """
        Devuelve las misiones almacenadas en el archivo YAML
        Returns:
            List[str]: Listado de Misiones
        """
        try:
            misiones_ar = []
            for misiones in data["settings"]["misiones"]:
                nombre_mision: str = misiones
                misiones_ar.append(nombre_mision)
            logger.info("Listado de misiones Creado")
            return misiones_ar
        except Exception as e:
            logger.error(f"Se ha producido un error en la generacion de misiones: {e}")
            return ["Unknown"]


    @staticmethod
    def nombres_abreviados() -> List[str]:
        """Retorna la lista de los nombres de las misiones, pero abreviados
        Returns:
            List[str]: Nombres de misiones abreviados
        """

        try:
            misiones_abreviados = []
            for mision, detalles in data["settings"]["misiones"].items():
                misiones_abreviados.append(detalles["nombreAbreviado"])
            logger.info("Listado de misiones abreviadas generado")
            return misiones_abreviados
        except Exception as e:
            logger.error(f"Se ha producido un error en la generacion de nombres abreviados misiones: {e}")
            misiones_abreviados.append("Unknow")


    @staticmethod
    def dispositivos() -> None:
        """Genera una impresion en consola de las misiones con
        sus respectivos dispositivos
        """
        try:
            for mision, detalles in data["settings"]["misiones"].items():
                nombre_mision = mision
                dispositivos = detalles["dispositivos"]
                print(f"Misión: {nombre_mision}")
                print("Dispositivos: ")
                for dispositivo in dispositivos:
                    print(f"  - {dispositivo}")
            logger.info("Misiones desplegadas en consola")
        except Exception as e:
            logger.error(f"Se ha producido un error en mostrar los archivos: {e}")


    @staticmethod
    def ciclo() -> float:
        """Retorna el ciclo de iteración que se encuentra en el archivo YAML
        Returns:
            float: Ciclo de iteración
        """
        try:
            ciclo: float = data["settings"]["ciclo_simulacion"]
            print(f"El ciclo actual es de: {ciclo} s \n")
            return ciclo
        except Exception as e:
            logger.error(f"Se ha producido un error en la lectura del ciclo: {e}")


    @staticmethod
    def cambiar_ciclo(ciclo: float) -> None:
        """Cambia el ciclo de iteracion en el archivo YAML

        Args:
            ciclo (float): Ciclo de iteracion
        """
        try:
            data["settings"]["ciclo_simulacion"] = ciclo
            with open(ruta, "w") as archivo:
                yaml.dump(data, archivo, default_flow_style=False)
            print("Datos modificados y almacenados correctamente")
            logger.info("Se ha modificado correctamente el ciclo de ejecucion")
        except Exception as e:
            logger.error(f"Se ha producido un error en la generacion de nombres abreviados misiones: {e}")


    @staticmethod
    def cambiar_min_archivos(archivos_min: int) -> None:
        """Cambia la cantidad minima de archivos que se pueden
        generar desde el archivo de configuracion YAML

        Args:
            archivos_min (int): recibe la cantidad de archivos minimos
        """
        try:
            data["settings"]["cantidad_min_archivos"] = archivos_min
            with open(ruta, "w") as archivo:
                yaml.dump(data, archivo, default_flow_style=False)
            print("Cantidad minima de archivos - Modificados y almacenados correctamente")
            logger.info("Cantidad Minima de archivos, modificados correctamente")
        except Exception as e:
            logger.error(f"Se ha producido un error en modificar la cantidad minima de archivos: {e}")


    @staticmethod
    def cambiar_max_archivos(archivos_max: int) -> None:
        """Cambia la cantidad maxima de archivos que se pueden crear en un
        ciclo de iteracion, esto editando el archivo YAML

        Args:
            archivos_max (int): Cantidad maxima de archivos a
            editar en el archivo YAML
        """
        try:
            data["settings"]["cantidad_max_archivos"] = archivos_max
            with open(ruta, "w") as archivo:
                yaml.dump(data, archivo, default_flow_style=False)
            print(" Datos modificados y almacenados correctamente")
            logger.info("Cantidad Maxima de archivos, modificados correctamente")
        except Exception as e:
            logger.error(f"Se ha producido un error en modificar la cantidad maxima de archivos: {e}")


    @staticmethod
    def nuevo_dispositivo(mision: int, nuevo_dispositivo: str) -> None:
        """Crea un dispositivo
        Args:
            mision (int): Numero de mision dependiendo la posicion
            nuevo_dispositivo (str): cadena de texto del dispositivo a eliminar
        """
        try:
            data["settings"]["misiones"][mision]["dispositivos"].append(nuevo_dispositivo)
            logger.info(f"Dispositivo añadido correctamente a la misión {mision}")
            with open(ruta, "w") as archivo:
                yaml.dump(data, archivo, default_flow_style=False)
            print(f'Se añadió el dispositivo {nuevo_dispositivo} correctamente a la misión {mision}')
        except Exception as e:
            logger.error(f"Se ha producido un error al ingresar un nuevo dispositivo: {e}")


    @staticmethod
    def eliminar_dispositivo(mision: int, dispositivo_a_eliminar: str) -> None:
        """Elimina un dispositivo seleccionado desde la consola
        Args:
            mision (int): Numero de mision dependiendo la posicion
            dispositivo_a_eliminar (str): cadena de texto del dispositivo a eliminar
        """
        try:
            data["settings"]["misiones"][mision]["dispositivos"].pop(dispositivo_a_eliminar)
            with open(ruta, "w") as archivo:
                yaml.dump(data, archivo, default_flow_style=False)
                print(" Datos modificados y almacenados correctamente")
            logger.info(f"Se ha eliminado el dispositivo {dispositivo_a_eliminar} correctamente a la mision {mision}")
        except Exception as e:
            print(f"el dispositivo seleccionado no existe para la misión {mision}")
            logger.error(f"Se ha producido un error al eliminar un nuevo dispositivo: {e}")




    @staticmethod
    def dispositivos_mision(num_mision: int) -> List[str]:
        """Retorna todos los dispostivos existentes por cada mision

        Args:
            num_mision (int): Numero de la mision, responde a la posicion del vector

        Returns:
            List[str]: Listado de dispositivos con respecto a la mision
        """
        try:
            mision: List[str] = Configuracion.misiones()
            dispositivos = data["settings"]["misiones"][mision[num_mision]]["dispositivos"]
            logger.info("Lista de dispositivos desplegada")
            return dispositivos
        except Exception as e:
            logger.error(f"Se ha producido un error al Listar las misiones: {e}")


    @staticmethod
    def estado() -> List[str]:
        """Enlista todos los estados posibles de un dispositivo, leidos desde el archivo YAML

        Returns:
            List[str]: Listado de posibles estados
        """
        try:
            estados = data["settings"]["estado_de_dispositivo"]
            logger.info("Listado de estados generado correctamente")
            return estados
        except Exception as e:
            logger.error(f"Se ha producido un error al mostrar los estados: {e}")


    @staticmethod
    def cantidad_min_archivos() -> int:
        """Retorna la cantidad minima de archivos a generar

        Returns:
            int: Cantidad Minima de archivos a generar
        """
        try:
            cantidad_min_archivos = data["settings"]["cantidad_min_archivos"]
            logger.info("Cantidad minima de archivos tomados correctamente")
            return int(cantidad_min_archivos)
        except Exception as e:
            logger.error(f"Se ha producido un error al tomar la cantidad minima de archivos: {e}")


    @staticmethod
    def cantidad_max_archivos() -> int:

        """Retorna la cantidad maxima de archivos

        Returns:
            int: Cantidad Maxima de archivos a generar
        """
        try:
            cantidad_max_archivos = data["settings"]["cantidad_max_archivos"]
            logger.info("Cantidad Maxima de archivos tomados correctamente")
            return int(cantidad_max_archivos)
        except Exception as e:
            logger.error(f"Se ha producido un error al tomar la cantidad maxima de archivos: {e}")
