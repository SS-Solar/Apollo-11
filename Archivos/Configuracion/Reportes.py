
import pandas as pd
import matplotlib.pyplot as plt

# DataFrame de ejemplo
data = {
    'Mision': ['ColonyMoon', 'ColonyMoon', 'ColonyMoon', 'GalaxyTwo', 'GalaxyTwo', 'OrbitOne', 'OrbitOne', 'UNKW'],
    'Dispositivo': ['CM-ASC-SPS', 'CM-S-EFAM', 'CM-S-CD', 'GT-PRR-TS', 'GT-S-SPS', 'OO-PRR-SPS', 'OO-S-SPS', 'unknown'],
    'Estado': ['Warning', 'killed', 'Good', 'Excelent', 'Unknown', 'Faulty', 'Excelent', 'unknown'],
    'Cantidad_Eventos': [1, 1, 1, 1, 2, 1, 1, 10]
}

df = pd.DataFrame(data)

# Establecer el índice del DataFrame para facilitar la manipulación
df.set_index(['Mision', 'Dispositivo', 'Estado'], inplace=True)

# a) Estándar de nombres de archivos
# Puedes imprimir el ejemplo del formato de nombre de archivo
print("Ejemplo de nombre de archivo:")
print(f"APLSTATS-AnalisisEventos-{pd.Timestamp.now().strftime('%d%m%y%H%M%S')}.log\n")

# b) Análisis de eventos
# Tabla de eventos
tabla_eventos = df[['Cantidad_Eventos']].unstack().fillna(0).astype(int)
print("Tabla de Análisis de Eventos:")
print(tabla_eventos)

# c) Gestión de desconexiones
# Tabla de desconexiones "unknown"
tabla_desconexiones = df[df['Estado'] == 'unknown'].groupby(['Mision', 'Dispositivo']).sum()['Cantidad_Eventos'].unstack().fillna(0).astype(int)
print("\nTabla de Desconexiones 'unknown':")
print(tabla_desconexiones)

# d) Consolidación de misiones
# Tabla de consolidación de misiones
tabla_consolidacion = df.groupby('Dispositivo').apply(lambda x: pd.Series({
    'Misiones': x.index.get_level_values('Mision').nunique(),
    'Inoperable': 'Si' if 'Faulty' in x.index.get_level_values('Estado') else 'No'
})).reset_index().set_index('Dispositivo')
print("\nTabla de Consolidación de Misiones:")
print(tabla_consolidacion)
