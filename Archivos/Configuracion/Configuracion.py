#import Clases.informacion.datos_de_identificacion as VACMARS

#Dependencias

import yaml
import os
import platform
from datetime import datetime, timedelta
import json
import pandas as pd
import shutil
import typing
import logging


# Variables locales usadas

misiones_ar = []
dispositivos_ar = []

ruta_absoluta = os.path.dirname(os.path.abspath(__file__))
ruta= os.path.join(ruta_absoluta, 'config.yaml')


with open(ruta, "r") as file:
    data=yaml.safe_load(file)

    # Nombres de misiones
def misiones():
        
    misiones_ar = []
      
    for misiones in data ["settings"]["misiones"]:
        nombre_mision= misiones
        misiones_ar.append(nombre_mision)
    
    return misiones_ar

def nombres_abreviados():
    misiones_abreviados = []
    for mision, detalles in data["settings"]["misiones"].items():
        nombre_mision = mision
        try:
            misiones_abreviados.append(detalles["nombreAbreviado"])
        except:
            misiones_abreviados.append("Unknow")
    return misiones_abreviados

def dispositivos ():
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

def ciclo():
    ciclo = data["settings"]["ciclo_simulacion"]
    print(f"El ciclo actual es de: {ciclo} s \n")
    return ciclo

def cambiar_ciclo (ciclo: int):
    data["settings"]["ciclo_simulacion"] = ciclo
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print(" Datos modificados y almacenados correctamente")

def cambiar_min_archivos (archivos_min: int):
    data["settings"]["cantidad_min_archivos"] = archivos_min
    with open(ruta, "w") as archivo:
        yaml.dump(data, archivo, default_flow_style=False)
    print(" Datos modificados y almacenados correctamente")

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

def gestion_desconexiones():
    dtf = crear_dataFrame()
    df_filtrado = dtf[dtf['Estado']=='Unknown']
    df_filtrado = df_filtrado.sort_values(by = 'Cantidad_Eventos', ascending= False)
    #Retorna un Dataframe con los dispositivos que se encuentran en Unknown para cada mision
    return df_filtrado.head(10)

def dispositivos_inoperables():
    data_total = crear_dataFrame()
    #Arroja el porcentaje de dispositivos inoperables de todas las misiones con respecto al total de dispositivos.
    df_inop = data_total[data_total['Estado']=='killed']
    porcentaje_inop = (int(df_inop.shape[0])/int(data_total.shape[0]))*100
    #Retorna la cantidad de disp inoperables de todas las misiones y su porcentaje
    return df_inop.shape[0], round(porcentaje_inop, 2)

def Porcentajes():
    data_total = crear_dataFrame()
    data_total= data_total.sort_values(by='Cantidad_Eventos', ascending=False)
    porcentaje = []
    total_eventos = data_total['Cantidad_Eventos'].sum()
    print(total_eventos)
    for per in range(data_total.shape[0]):
        p_calculado = data_total.iloc[per,3]/total_eventos*100
        porcentaje.append(round(p_calculado,2))
    data_total['Porcentaje_Eventos']= porcentaje
    return data_total



df= crear_dataFrame()
print(df)