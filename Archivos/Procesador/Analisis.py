from Archivos.Configuracion.Configuracion import Configuracion
import json
import pandas as pd
import shutil
from Archivos.Configuracion.Logger import Logger
from typing import List
import os

logger = Logger

ruta_absoluta = os.path.dirname(os.path.abspath(__file__))

class Analisis:
    
    @staticmethod
    def crear_dataFrame() -> str:
        """Crea un dataFrame a partir de los reportes y analisis de los eventos
        Returns:
            str: Dataframe que resume los eventos ocurridos en cada mision
        """
        eventos: any = Analisis.analisis_eventos()
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


    @staticmethod
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


    @staticmethod
    def eventos() -> any:
        """Retorna los eventos por mision en donde se evidencia el estado de los dispositivos

        Returns:
            str: tabla de eventos de los dispositivos
        """
        try:
            df: any = Analisis.crear_dataFrame()
            df.set_index(['Mision', 'Dispositivo', 'Estado'], inplace=True)
            tabla_eventos: any = df[['Cantidad_Eventos']].unstack().fillna(0).astype(int)
            logger.info("Se ha generado correctamente la tabla de eventos")
            return tabla_eventos
        except Exception as e:
            logger.error(f"Se ha producido un error al generar la tabla de eventos: {e}")


    @staticmethod
    def gestion_desconexiones() -> any:
        """Retorna de el listado de eventos, los dispositivos que se encuentren en un estado desconocido

        Returns:
            str: dispositivos en estado UNKW
        """
        try:
            dtf: any = Analisis.crear_dataFrame()
            df_filtrado: any = dtf[dtf['Estado'] == 'Unknown']
            df_filtrado: str = df_filtrado.sort_values(by='Cantidad_Eventos', ascending=False).head(10).groupby(['Mision', 'Dispositivo']).agg({'Cantidad_Eventos': 'sum'})
            logger.info("Gestion de desconexiones generado correctamente")
            return df_filtrado
        except Exception as e:
            logger.error(f"Se ha producido un error al generar la tabla de eventos: {e}")


    @staticmethod
    def dispositivos_inoperables() -> [str, str, float]:
        """Retorna el analisis de los dispositivoas con estado Killed

        Returns:
            [str, str, float]: retorna el normbre de la mision, sigue el dispositivo y finaliza con el porcentaje
        """
        try:
            data_total: str = Analisis.crear_dataFrame()
            df_inop: any = data_total[data_total['Estado'] == 'killed'].groupby(['Mision', 'Dispositivo']).agg({'Cantidad_Eventos': 'sum'})
            porcentaje_inop: float = (int(df_inop.shape[0]) / int(data_total.shape[0])) * 100
            logger.info('Se ha generado correctamente el reporte de dispositivos inoperables')
            return df_inop, df_inop.shape[0], round(porcentaje_inop, 2)
        except Exception as e:
            logger.error(f"Se ha producido un error al generar las estadisticas de los dispositivos inoperables: {e}")

    @staticmethod
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

    @staticmethod
    def Porcentajes() -> any:
        """Retorna una tabla con los porcentajes de cada mision, porecntajes de desconexion

        Returns:
            any: Porcentajes
        """
        try:
            data_total: str = Analisis.crear_dataFrame()
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
