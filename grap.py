import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo CSV
archivo_egresos = 'Listado_egresos_hospitalizados_enero_2022_junio2024.csv'
archivo_nuevos_pacientes = 'Listado_pacientes_nuevos_inen_enero2022_junio2024.csv'

# Leer los datos en DataFrames de pandas
df_egresos = pd.read_csv(archivo_egresos)
df_nuevos_pacientes = pd.read_csv(archivo_nuevos_pacientes)

# Convertir columnas de fechas a formato datetime para análisis temporal
df_egresos['FECHA_INGRESO'] = pd.to_datetime(df_egresos['FECHA_INGRESO'])
df_egresos['FECHA_EGRESO'] = pd.to_datetime(df_egresos['FECHA_EGRESO'])
df_nuevos_pacientes['FECHA_INGRESO'] = pd.to_datetime(df_nuevos_pacientes['FECHA_INGRESO'])

# Ejemplo de gráfico 1: Número de egresos por mes
df_egresos['MES_EGRESO'] = df_egresos['FECHA_EGRESO'].dt.to_period('M')
egresos_por_mes = df_egresos.groupby('MES_EGRESO').size()

plt.figure(figsize=(10, 6))
egresos_por_mes.plot(kind='bar', color='skyblue')
plt.title('Número de Egresos por Mes')
plt.xlabel('Mes')
plt.ylabel('Cantidad de Egresos')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Ejemplo de gráfico 2: Distribución de la duración de la estadía
df_egresos['DURACION_ESTADIA'] = (df_egresos['FECHA_EGRESO'] - df_egresos['FECHA_INGRESO']).dt.days

plt.figure(figsize=(10, 6))
sns.histplot(df_egresos['DURACION_ESTADIA'], bins=30, kde=True)
plt.title('Distribución de la Duración de la Estadía')
plt.xlabel('Días de Estadía')
plt.ylabel('Cantidad de Pacientes')
plt.show()

# Ejemplo de gráfico 3: Comparación de pacientes nuevos y egresos por mes
df_nuevos_pacientes['MES_INGRESO'] = df_nuevos_pacientes['FECHA_INGRESO'].dt.to_period('M')
nuevos_por_mes = df_nuevos_pacientes.groupby('MES_INGRESO').size()

plt.figure(figsize=(10, 6))
plt.plot(egresos_por_mes.index.astype(str), egresos_por_mes.values, label='Egresos')
plt.plot(nuevos_por_mes.index.astype(str), nuevos_por_mes.values, label='Nuevos Pacientes')
plt.title('Comparación de Egresos y Nuevos Pacientes por Mes')
plt.xlabel('Mes')
plt.ylabel('Cantidad')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
