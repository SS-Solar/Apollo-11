# Dependencias
import yaml
import os
import json
import pandas as pd
from typing import List
import shutil
from Archivos.Configuracion.logger import logger

# Variables locales usadas

misiones_ar = List[str]
dispositivos_ar = List[str]
ruta_absoluta = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(ruta_absoluta, 'config.yaml')

# Apertura de archivo de configuracion para su respectivo uso

with open(ruta, "r") as file:
    data = yaml.safe_load(file)


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
        misiones_ar = ["Unknown"]


def nombres_abreviados() -> List[str]:
    """Retorna la lista de los nombres de las misiones, pero abreviados
    Returns:
        List[str]: Nombres de misiones abreviados
    """

    try:
        misiones_abreviados = List[str]
        for mision, detalles in data["settings"]["misiones"].items():
            misiones_abreviados.append(detalles["nombreAbreviado"])
        logger.info("Listado de misiones abreviadas generado")
        return misiones_abreviados
    except Exception as e:
        logger.error(f"Se ha producido un error en la generacion de nombres abreviados misiones: {e}")
        misiones_abreviados.append("Unknow")


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


def nuevo_dispositivo(mision: int, nuevo_dispositivo: str) -> None:
    """Añade un duevo dispositivo segun la mision seleccionada, añadiendo
    el dispositivo segun la entrada del segundo argumento

    Args:
        mision (int): Toma la mision dependiendo el numero de posicion de la mision.
        nuevo_dispositivo (str): Cadena de texto que recibe el nombre del dispositivo
        para añadirla al archimo YAML
    """
    try:
        data["settings"]["misiones"][mision]["dispositivos"].append(nuevo_dispositivo)
        mision: str = data["settings"]["misiones"][mision]
        logger.info("Dispositivo añadido correctamente a la mision " + mision)
        with open(ruta, "w") as archivo:
            yaml.dump(data, archivo, default_flow_style=False)
        print(f'Se añadió el dispositivo {nuevo_dispositivo} correctamente a la misión {mision}')
        logger.info(f'Se añadió el dispositivo {nuevo_dispositivo} correctamente a la misión {mision}')
    except Exception as e:
        logger.error(f"Se ha producido un error al ingresar un nuevo dispositivo: {e}")


def eliminar_dispositivo(mision: int, dispositivo_a_eliminar: str) -> None:
    """Elimina un dispositivo seleccionado desde la consola
    Args:
        mision (int): Numero de mision dependiendo la posicion
        dispositivo_a_eliminar (str): cadena de texto del dispositivo a eliminar
    """
    try:
        dispo = data["settings"]["misiones"][mision]["dispositivos"].pop(dispositivo_a_eliminar)
        with open(ruta, "w") as archivo:
            yaml.dump(data, archivo, default_flow_style=False)
            print(" Datos modificados y almacenados correctamente")
        logger.info("Se ha eliminado el dispositivo " + dispo)
    except Exception as e:
        print(f"el dispositivo seleccionado no existe para la misión {mision}")
        logger.error(f"Se ha producido un error al eliminar un nuevo dispositivo: {e}")


def dispositivos_mision(num_mision: int) -> List[str]:
    """Retorna todos los dispostivos existentes por cada mision

    Args:
        num_mision (int): Numero de la mision, responde a la posicion del vector

    Returns:
        List[str]: Listado de dispositivos con respecto a la mision
    """
    try:
        mision: List[str] = misiones()
        dispositivos = data["settings"]["misiones"][mision[num_mision]]["dispositivos"]
        logger.info("Lista de dispositivos desplegada")
        return dispositivos
    except Exception as e:
        logger.error(f"Se ha producido un error al Listar las misiones: {e}")


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


def crear_dataFrame() -> str:
    """Crea un dataFrame a partir de los reportes y analisis de los eventos
    Returns:
        str: Dataframe que resume los eventos ocurridos en cada mision
    """
    eventos: any = analisis_eventos()
    data_frame: List[any] = ["Mision", "Dispositivo", "Estado", "Cantidad_Eventos"]
    df: any = pd.DataFrame(columns=data_frame)
    nuevos_registros: List[any] = []
    try:
        for llave, valor in eventos.items():
            mision, device, status = llave
            cantidad: int = valor
            nuevo_registro: dict[str, any] = {"Mision": mision, "Dispositivo": device, "Estado": status, "Cantidad_Eventos": cantidad}
            nuevos_registros.append(nuevo_registro)
        df: any = pd.concat([df, pd.DataFrame(nuevos_registros)], ignore_index=True)
        logger.info("DataFrame creado correctamente")
        return df
    except Exception as e:
        logger.error(f"Se ha generado un error al intentar generar un dataframe: {e}")


def analisis_eventos() -> dict:
    """Genera un Documento con el resumen y analisis de los eventos

    Returns:
        dict: analisis de eventos
    """
    ruta_script: str = os.path.abspath(__file__)
    ruta_logs: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ruta_script))), "Archivos", "Logs")
    lista_carpetas: List[str] = [nombre for nombre in os.listdir(ruta_logs)]
    registro_eventos = {}
    try:
        for archivo_carpeta in lista_carpetas:
            ruta_carpeta: str = os.path.join(ruta_logs, archivo_carpeta)
            lista_archivos: str = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.log')]
            for a in lista_archivos:
                ruta_archivos: str = os.path.join(ruta_carpeta, a)
                with open(ruta_archivos, 'r') as arch_log:
                    archivo: str = arch_log.read()
                    registro_dict: str = json.loads(archivo)
                    mision: str = registro_dict['mision']
                    dispositivo: str = registro_dict['device_type']
                    estado: str = registro_dict['device_status']
                    llave: str = (mision, dispositivo, estado)
                    registro_eventos[llave] = registro_eventos.get(llave, 0) + 1
        logger.info("Se han analizado correctamente los registros")
        return registro_eventos
    except Exception as e:
        logger.error(f"Se ha producido un error al analizar los eventos: {e}")


def eventos() -> any:
    """Retorna los eventos por mision en donde se evidencia el estado de los dispositivos

    Returns:
        str: tabla de eventos de los dispositivos
    """
    try:
        df: any = crear_dataFrame()
        df.set_index(['Mision', 'Dispositivo', 'Estado'], inplace=True)
        tabla_eventos: any = df[['Cantidad_Eventos']].unstack().fillna(0).astype(int)
        logger.info("Se ha generado correctamente la tabla de eventos")
        return tabla_eventos
    except Exception as e:
        logger.error(f"Se ha producido un error al generar la tabla de eventos: {e}")


def gestion_desconexiones() -> any:
    """Retorna de el listado de eventos, los dispositivos que se encuentren en un estado desconocido

    Returns:
        str: dispositivos en estado UNKW
    """
    try:
        dtf: any = crear_dataFrame()
        df_filtrado: any = dtf[dtf['Estado'] == 'Unknown']
        df_filtrado: str = df_filtrado.sort_values(by='Cantidad_Eventos', ascending=False).head(10).groupby(['Mision', 'Dispositivo']).agg({'Cantidad_Eventos': 'sum'})
        logger.info("Gestion de desconexiones generado correctamente")
        return df_filtrado
    except Exception as e:
        logger.error(f"Se ha producido un error al generar la tabla de eventos: {e}")


def dispositivos_inoperables() -> [str, str, float]:
    """Retorna el analisis de los dispositivoas con estado Killed

    Returns:
        [str, str, float]: retorna el normbre de la mision, sigue el dispositivo y finaliza con el porcentaje
    """
    try:
        data_total: str = crear_dataFrame()
        df_inop: any = data_total[data_total['Estado'] == 'killed'].groupby(['Mision', 'Dispositivo']).agg({'Cantidad_Eventos': 'sum'})
        porcentaje_inop: float = (int(df_inop.shape[0]) / int(data_total.shape[0])) * 100
        logger.info('Se ha generado correctamente el reporte de dispositivos inoperables')
        return df_inop, df_inop.shape[0], round(porcentaje_inop, 2)
    except Exception as e:
        logger.error(f"Se ha producido un error al generar las estadisticas de los dispositivos inoperables: {e}")


# def Porcentajes() -> any:
#     """Retorna una tabla con los porcentajes de cada mision, porecntajes de desconexion

#     Returns:
#         any: Porcentajes
#     """
#     try:
#         data_total: str = crear_dataFrame()
#         total_eventos: int = data_total['Cantidad_Eventos'].sum()
#         formato_centro = lambda x: f'{"{:^35}".format(x)}'
#         data_total['Porcentaje de datos Generados(%)'] = (data_total['Cantidad_Eventos'] / total_eventos * 100).apply(lambda x: round(x, 2)).apply(formato_centro)
#         data_total: any = data_total.drop(['Estado','Cantidad_Eventos'], axis=1)
#         data_total.set_index(['Mision', 'Dispositivo'], inplace=True)
#         logger.info("Se ha generado correctamente los porcentajes de los datos (Configuracion/Porcentajes())")
#         return data_total
#     except Exception as e:
#         logger.error(f"Se ha producido un error al generar los porcentajes (Configuracion/Porcentajes()): {e}")


def Crear_copia() -> None:
    """Crea una copia del archivo del ultimo reporte generado
    """
    try:
        ruta_script: str = os.path.abspath(__file__)
        ruta_reporte: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ruta_script))), "Archivos", "Reportes")
        lista_reporte: List[str] = [rep for rep in os.listdir(ruta_reporte) if rep.endswith('.log')]
        archivo: str = lista_reporte[-1]
        if lista_reporte:
            archivo_original: str = os.path.join(ruta_reporte, archivo)
            ruta_copia: str = os.path.join("Archivos", "Reportes", "Copias", f"COPIA-{archivo}")
            shutil.copyfile(archivo_original, ruta_copia)
            print("Copia creada exitosamente.")
            logger.info("Copia creada exitosamente de el reporte de .logs")
        else:
            print("No se encontraron archivos .log para copiar.")
    except Exception as e:
        logger.error(f"Se ha producido un error al crear copia de .logs: {e}")


def Porcentajes() -> any:
    """Retorna una tabla con los porcentajes de cada mision, porecntajes de desconexion

    Returns:
        any: Porcentajes
    """
    try:
        data_total: str = crear_dataFrame()
        total_eventos: any = data_total['Cantidad_Eventos'].sum()
        formato_centro: str = lambda x: f'{"{:^35}".format(x)}'
        data_total['Porcentaje de datos Generados(%)'] = (data_total['Cantidad_Eventos'] / total_eventos * 100).apply(lambda x: round(x, 2)).apply(formato_centro)
        data_total: any = data_total.drop(['Estado', 'Cantidad_Eventos'], axis=1)
        df_colonymoon: any = data_total[data_total['Mision'] == 'ColonyMoon'].set_index('Dispositivo').drop('Mision', axis=1)
        df_galaxytwo: any = data_total[data_total['Mision'] == 'GalaxyTwo'].set_index('Dispositivo').drop('Mision', axis=1)
        df_orbione: any = data_total[data_total['Mision'] == 'OrbitOne'].set_index('Dispositivo').drop('Mision', axis=1)
        df_vacmars: any = data_total[data_total['Mision'] == 'VacMars'].set_index('Dispositivo').drop('Mision', axis=1)
        unk: any = data_total[data_total['Mision'] == 'UNKW'].set_index('Dispositivo').drop('Mision', axis=1)
        logger.info("Se ha generado correctamente los porcentajes de los datos")
        return df_colonymoon, df_galaxytwo, df_orbione, df_vacmars, unk
    except Exception as e:
        logger.error(f"Se ha producido un error al generar los porcentajes : {e}")
