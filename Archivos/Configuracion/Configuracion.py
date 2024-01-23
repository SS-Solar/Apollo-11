# Dependencias
import yaml
import os
import json
import pandas as pd
from typing import List
import shutil

# Variables locales usadas
misiones_ar = List[str]
dispositivos_ar = List[str]
ruta_absoluta = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(ruta_absoluta, 'config.yaml')
# Apertura de archivo de configuracion para su respectivo uso
with open(ruta, "r") as file:
    data = yaml.safe_load(file)


def misiones() -> List[str]:
    """_summary_
    Devuelve las misiones almacenadas en el archivo YAML
    Returns:
        List[str]: Listado de Misiones
    """
    misiones_ar = []
    for misiones in data["settings"]["misiones"]:
        nombre_mision = misiones
        misiones_ar.append(nombre_mision)
    return misiones_ar


def nombres_abreviados() -> List[str]:
    """Retorna la lista de los nombres de las misiones, pero abreviados
    Returns:
        List[str]: Nombres de misiones abreviados
    """
    misiones_abreviados = List[str]
    for mision, detalles in data["settings"]["misiones"].items():
        try:
            misiones_abreviados.append(detalles["nombreAbreviado"])
        except Exception as e:
            e.error('The user does not exist with that ID')
            misiones_abreviados.append("Unknow")
    return misiones_abreviados


def dispositivos() -> None:
    """Genera una impresion en consola de las misiones con
    sus respectivos dispositivos
    """
    for mision, detalles in data["settings"]["misiones"].items():
        nombre_mision = mision
        dispositivos = detalles["dispositivos"]
        print(f"Misión: {nombre_mision}")
        print("Dispositivos: ")
        for dispositivo in dispositivos:
            print(f"  - {dispositivo}")


def ciclo() -> float:
    """Retorna el ciclo de iteración que se encuentra en el archivo YAML
    Returns:
        float: Ciclo de iteración
    """
    ciclo: float = data["settings"]["ciclo_simulacion"]
    print(f"El ciclo actual es de: {ciclo} s \n")
    return ciclo


def cambiar_ciclo(ciclo: float) -> None:
    """Cambia el ciclo de iteracion en el archivo YAML

    Args:
        ciclo (float): Ciclo de iteracion
    """
    data["settings"]["ciclo_simulacion"] = ciclo
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print(" Datos modificados y almacenados correctamente")


def cambiar_min_archivos(archivos_min: int) -> None:
    """Cambia la cantidad minima de archivos que se pueden
    generar desde el archivo de configuracion YAML

    Args:
        archivos_min (int): recibe la cantidad de archivos minimos
    """
    data["settings"]["cantidad_min_archivos"] = archivos_min
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print("Cantidad minima de archivos - Modificados y almacenados correctamente")


def cambiar_max_archivos(archivos_max: int) -> None:
    """Cambia la cantidad maxima de archivos que se pueden crear en un
    ciclo de iteracion, esto editando el archivo YAML

    Args:
        archivos_max (int): Cantidad maxima de archivos a
        editar en el archivo YAML
    """
    data["settings"]["cantidad_max_archivos"] = archivos_max
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print(" Datos modificados y almacenados correctamente")


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
    except Exception as e:
        data["settings"]["misiones"][mision]["dispositivos"] = []
        data["settings"]["misiones"][mision]["dispositivos"].append(nuevo_dispositivo)
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print(f'Se añadió el dispositivo {nuevo_dispositivo} correctamente a la misión {mision}.')


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
    except Exception as e:
        print(f"el dispositivo seleccionado no existe para la misión {mision}")


def dispositivos_mision(num_mision: int) -> List[str]:
    """Retorna todos los dispostivos existentes por cada mision

    Args:
        num_mision (int): Numero de la mision, responde a la posicion del vector

    Returns:
        List[str]: Listado de dispositivos con respecto a la mision
    """
    mision: List[str] = misiones()
    dispositivos = data["settings"]["misiones"][mision[num_mision]]["dispositivos"]
    return dispositivos


def estado() -> List[str]:
    """Enlista todos los estados posibles de un dispositivo, leidos desde el archivo YAML

    Returns:
        List[str]: Listado de posibles estados
    """
    estados = data["settings"]["estado_de_dispositivo"]
    return estados


def cantidad_min_archivos() -> int:
    """Retorna la cantidad minima de archivos a generar

    Returns:
        int: Cantidad Minima de archivos a generar
    """
    cantidad_min_archivos = data["settings"]["cantidad_min_archivos"]
    return int(cantidad_min_archivos)


def cantidad_max_archivos() -> int:

    """Retorna la cantidad maxima de archivos

    Returns:
        int: Cantidad Maxima de archivos a generar
    """
    cantidad_max_archivos = data["settings"]["cantidad_max_archivos"]
    return int(cantidad_max_archivos)


def crear_dataFrame() -> str:
    """Crea un dataFrame a partir de los reportes y analisis de los eventos
    Returns:
        str: Dataframe que resume los eventos ocurridos en cada mision
    """
    eventos: str = analisis_eventos()
    data_frame: List[str] = ["Mision", "Dispositivo", "Estado", "Cantidad_Eventos"]
    df: any = pd.DataFrame(columns=data_frame)
    nuevos_registros: List[str] = []
    for llave, valor in eventos.items():
        mision, device, status = llave
        cantidad: int = valor
        nuevo_registro: dict[str, any] = {"Mision": mision, "Dispositivo": device, "Estado": status, "Cantidad_Eventos": cantidad}
        nuevos_registros.append(nuevo_registro)
    df: any = pd.concat([df, pd.DataFrame(nuevos_registros)], ignore_index=True)
    return df


def analisis_eventos() -> dict:

    """Genera un Documento con el resumen y analisis de los eventos

    Returns:
        dict: analisis de eventos
    """
    ruta_script: str = os.path.abspath(__file__)
    ruta_logs: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ruta_script))), "Archivos", "Logs")
    lista_carpetas: List[str] = [nombre for nombre in os.listdir(ruta_logs)]
    registro_eventos = {}
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
                registro_eventos[llave] = registro_eventos.get(llave,0)+1
    return registro_eventos


def eventos() -> str:
    """Retorna los eventos por mision en donde se evidencia el estado de los dispositivos

    Returns:
        str: tabla de eventos de los dispositivos
    """
    df: str = crear_dataFrame()
    df.set_index(['Mision', 'Dispositivo', 'Estado'], inplace=True)
    tabla_eventos: any = df[['Cantidad_Eventos']].unstack().fillna(0).astype(int)
    return tabla_eventos


def gestion_desconexiones() -> str:
    """Retorna de el listado de eventos, los dispositivos que se encuentren en un estado desconocido

    Returns:
        str: dispositivos en estado UNKW
    """
    dtf: str = crear_dataFrame()
    df_filtrado: str = dtf[dtf['Estado']=='Unknown']
    df_filtrado: str = df_filtrado.sort_values(by='Cantidad_Eventos', ascending=False).head(10).groupby(['Mision', 'Dispositivo']).agg({'Cantidad_Eventos': 'sum'})
    return df_filtrado


def dispositivos_inoperables() -> [str, str, float]:
    """Retorna el analisis de los dispositivoas con estado Killed

    Returns:
        [str, str, float]: retorna el normbre de la mision, sigue el dispositivo y finaliza con el porcentaje
    """
    data_total: str = crear_dataFrame()
    df_inop: any = data_total[data_total['Estado']=='killed'].groupby(['Mision', 'Dispositivo']).agg({'Cantidad_Eventos': 'sum'})
    porcentaje_inop: float = (int(df_inop.shape[0])/int(data_total.shape[0]))*100
    return df_inop, df_inop.shape[0], round(porcentaje_inop, 2)


def Porcentajes() -> any:
    """Retorna una tabla con los porcentajes de cada mision, porecntajes de desconexion

    Returns:
        any: Porcentajes
    """
    data_total = crear_dataFrame()
    total_eventos = data_total['Cantidad_Eventos'].sum()
    formato_centro = lambda x: f'{"{:^35}".format(x)}'
    data_total['Porcentaje de datos Generados(%)'] = (data_total['Cantidad_Eventos'] / total_eventos * 100).apply(lambda x: round(x, 2)).apply(formato_centro)
    data_total= data_total.drop(['Estado','Cantidad_Eventos'], axis=1)
    df_colonymoon = data_total[data_total['Mision'] == 'ColonyMoon'].set_index('Dispositivo').drop('Mision', axis=1)
    df_galaxytwo = data_total[data_total['Mision'] == 'GalaxyTwo'].set_index('Dispositivo').drop('Mision', axis=1)
    df_orbione = data_total[data_total['Mision'] == 'OrbitOne'].set_index('Dispositivo').drop('Mision', axis=1)
    df_vacmars = data_total[data_total['Mision'] == 'VacMars'].set_index('Dispositivo').drop('Mision', axis=1)
    unk = data_total[data_total['Mision'] == 'UNKW'].set_index('Dispositivo').drop('Mision', axis=1)
    return df_colonymoon,df_galaxytwo,df_orbione,df_vacmars,unk


def Crear_copia() -> None:
    """Crea una copia del archivo del ultimo reporte generado
    """
    ruta_script: str = os.path.abspath(__file__)
    ruta_reporte = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ruta_script))), "Archivos", "Reportes")
    lista_reporte = [rep for rep in os.listdir(ruta_reporte) if rep.endswith('.log')]
    archivo = lista_reporte[-1]
    if lista_reporte:
        archivo_original = os.path.join(ruta_reporte, archivo)
        ruta_copia = os.path.join("Archivos", "Reportes", "Copias", f"COPIA-{archivo}") 
        shutil.copyfile(archivo_original, ruta_copia)
        print("Copia creada exitosamente.")
    else:
        print("No se encontraron archivos .log para copiar.")
