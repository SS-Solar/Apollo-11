#Dependencias
import yaml
import os
from datetime import datetime, timedelta
import json
import pandas as pd
from typing import List

# Variables locales usadas
misiones_ar = List[str]
dispositivos_ar = List[str]
ruta_absoluta = os.path.dirname(os.path.abspath(__file__))
ruta= os.path.join(ruta_absoluta, 'config.yaml')
# Apertura de archivo de configuracion para su respectivo uso
with open(ruta, "r") as file:
    data=yaml.safe_load(file)

def misiones() -> List[str]:
    """_summary_
    Devuelve las misiones almacenadas en el archivo YAML
    Returns:
        List[str]: Listado de Misiones
    """
    misiones_ar = []
    for misiones in data ["settings"]["misiones"]:
        nombre_mision= misiones
        misiones_ar.append(nombre_mision)
    return misiones_ar

def nombres_abreviados() -> List[str]:
    """Retorna la lista de los nombres de las misiones, pero abreviados

    Returns:
        List[str]: Nombres de misiones abreviados
    """
    misiones_abreviados = List[str]
    for mision, detalles in data["settings"]["misiones"].items():
        nombre_mision :[str] = mision
        try:
            misiones_abreviados.append(detalles["nombreAbreviado"])
        except:
            misiones_abreviados.append("Unknow")
    return misiones_abreviados

def dispositivos ()-> None:
    """Genera una impresion en consola de las misiones con
    sus respectivos dispositivos
    """
    for mision, detalles in data["settings"]["misiones"].items():
        try:
            nombre_mision = mision
            dispositivos = detalles["dispositivos"]
            print(f"Misión: {nombre_mision}")
            print("Dispositivos: ")
            for dispositivo in dispositivos:
                print(f"  - {dispositivo}")
        except:
            pass

def ciclo() -> float:
    """Retorna el ciclo de iteración que se encuentra en el archivo YAML
    Returns:
        float: Ciclo de iteración
    """
    ciclo:float = data["settings"]["ciclo_simulacion"]
    print(f"El ciclo actual es de: {ciclo} s \n")
    return ciclo

def cambiar_ciclo (ciclo: float) -> None:
    """Cambia el ciclo de iteracion en el archivo YAML

    Args:
        ciclo (float): Ciclo de iteracion 
    """
    data["settings"]["ciclo_simulacion"] = ciclo
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print(" Datos modificados y almacenados correctamente")

def cambiar_min_archivos (archivos_min: int) ->None:
    """Cambia la cantidad minima de archivos que se pueden generar desde el archivo de configuracion YAML

    Args:
        archivos_min (int): recibe la cantidad de archivos minimos
    """
    data["settings"]["cantidad_min_archivos"] = archivos_min
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print(" Cantidad minima de archivos - Modificados y almacenados correctamente")

def cambiar_max_archivos (archivos_max: int):
    data["settings"]["cantidad_max_archivos"] = archivos_max
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print(" Datos modificados y almacenados correctamente")   

def nuevo_dispositivo (mision,nuevo_dispositivo):
    try:
        data["settings"]["misiones"][mision]["dispositivos"].append(nuevo_dispositivo)
    except:
        data["settings"]["misiones"][mision]["dispositivos"] = []
        data["settings"]["misiones"][mision]["dispositivos"].append(nuevo_dispositivo)
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print(f'Se añadió el dispositivo {nuevo_dispositivo} correctamente a la misión {mision}.')

def eliminar_dispositivo (mision,dispositivo_a_eliminar):
    try:
        data["settings"]["misiones"][mision]["dispositivos"].pop(dispositivo_a_eliminar)
        with open(ruta, "w") as archivo:
            yaml.dump(data, archivo, default_flow_style=False)
            print(" Datos modificados y almacenados correctamente")
    except:
        print(f"el dispositivo seleccionado no existe para la misión {mision}")

def dispositivos_mision(num_mision):
    mision = misiones()
    dispositivos = data["settings"]["misiones"][mision[num_mision]]["dispositivos"]
    return dispositivos

def estado():
    estados = data["settings"]["estado_de_dispositivo"]
    return estados

def cantidad_min_archivos():
    cantidad_min_archivos = data["settings"]["cantidad_min_archivos"]
    return int(cantidad_min_archivos)

def cantidad_max_archivos():
    cantidad_max_archivos = data["settings"]["cantidad_max_archivos"]
    return int(cantidad_max_archivos)


def crear_dataFrame():
    eventos = analisis_eventos()
    data_frame = ["Mision", "Dispositivo", "Estado", "Cantidad_Eventos"]
    df = pd.DataFrame(columns= data_frame)
    nuevos_registros = []
    for llave, valor in eventos.items():
        mision, device, status = llave
        cantidad = valor
        nuevo_registro = {"Mision": mision, "Dispositivo": device, "Estado": status, "Cantidad_Eventos": cantidad}
        nuevos_registros.append(nuevo_registro)
    # Concatenar los nuevos registros al DataFrame original
    df = pd.concat([df, pd.DataFrame(nuevos_registros)], ignore_index=True)

    return df

def analisis_eventos():
    ruta_script = os.path.abspath(__file__) 
    # Construir la ruta relativa al directorio 'Logs' dentro de 'Archivos'
    ruta_logs = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(ruta_script))), "Archivos", "Logs")
    lista_carpetas = [nombre for nombre in os.listdir(ruta_logs)]
    registro_eventos = {}
    for archivo_carpeta in lista_carpetas:
        #Ruta relativa a las carpetas dentro del directorio Logs
        ruta_carpeta = os.path.join(ruta_logs, archivo_carpeta)
        lista_archivos = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith('.log')]
        for a in lista_archivos:
            ruta_archivos = os.path.join(ruta_carpeta, a)
            with open(ruta_archivos, 'r') as arch_log: #Abre el archivo en modo lectura
                archivo = arch_log.read()
                registro_dict = json.loads(archivo) #Convertir el archivo json a diccionario
                mision= registro_dict['mision']
                dispositivo = registro_dict['device_type']
                estado = registro_dict['device_status']
                llave = (mision,dispositivo,estado)
                registro_eventos[llave]= registro_eventos.get(llave,0)+1 #Incrememta el valor de la llave obtenida
    #Retorna un diccionario con los datos optenidos en los archivos logs       
    return registro_eventos

def eventos():
    df= crear_dataFrame()
    df.set_index(['Mision', 'Dispositivo', 'Estado'], inplace=True)
    tabla_eventos = df[['Cantidad_Eventos']].unstack().fillna(0).astype(int)
    return tabla_eventos

def gestion_desconexiones():
    dtf = crear_dataFrame()
    df_filtrado = dtf[dtf['Estado']=='Unknown']
    df_filtrado = df_filtrado.sort_values(by = 'Cantidad_Eventos', ascending= False).head(10).groupby(['Mision', 'Dispositivo']).agg({'Cantidad_Eventos': 'sum'})
    #Retorna un Dataframe con los dispositivos que se encuentran en Unknown para cada mision
    return df_filtrado

def dispositivos_inoperables():
    data_total = crear_dataFrame()
    #Arroja el porcentaje de dispositivos inoperables de todas las misiones con respecto al total de dispositivos.
    df_inop = data_total[data_total['Estado']=='killed'].groupby(['Mision', 'Dispositivo']).agg({'Cantidad_Eventos': 'sum'})
    porcentaje_inop = (int(df_inop.shape[0])/int(data_total.shape[0]))*100
    #Retorna la cantidad de disp inoperables de todas las misiones y su porcentaje
    return df_inop, df_inop.shape[0], round(porcentaje_inop, 2)

def Porcentajes():
    data_total = crear_dataFrame()
    total_eventos = data_total['Cantidad_Eventos'].sum()
    formato_centro = lambda x: f'{"{:^35}".format(x)}'
    data_total['Porcentaje de datos Generados(%)'] = (data_total['Cantidad_Eventos'] / total_eventos * 100).apply(lambda x: round(x, 2)).apply(formato_centro)
    data_total= data_total.drop(['Estado','Cantidad_Eventos'], axis=1)
    data_total.set_index(['Mision', 'Dispositivo'], inplace=True)
    return data_total
