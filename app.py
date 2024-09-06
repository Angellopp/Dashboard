import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd

# URL del archivo GeoJSON de los departamentos de Perú
geojson_url = 'https://raw.githubusercontent.com/juaneladio/peru-geojson/master/peru_departamental_simple.geojson'

# Cargar los datos de los egresos
url_csv = 'https://raw.githubusercontent.com/Angellopp/Dashboard/main/Listado_egresos_hopitalizados_enero_2022_junio2024.csv'
df = pd.read_csv(url_csv, encoding='latin-1')

# Extraer el departamento de la columna LUGAR_RESIDENCIA
df['DEPARTAMENTO'] = df['LUGAR_RESIDENCIA'].str.split('-').str[0].str.strip().str.upper()

# Contar la cantidad de egresos por departamento
egresos_por_departamento = df['DEPARTAMENTO'].value_counts().reset_index()
egresos_por_departamento.columns = ['Departamento', 'Cantidad']

# Mostrar los datos de egresos
st.write("Datos de egresos por departamento:")
st.write(egresos_por_departamento)

# Cargar el GeoJSON de Perú
peru_geojson = gpd.read_file(geojson_url)
geojson = px.data.election_geojson()


# Unir los datos de egresos con el GeoJSON por departamento
# peru_geojson['Departamento'] = peru_geojson['NOMBDEP'].str.strip().str.upper()
# merged = peru_geojson.merge(egresos_por_departamento, on='Departamento', how='left')

# Rellenar los valores NaN con 0
# merged['Cantidad'] = merged['Cantidad'].fillna(0)

# Mostrar los datos unidos
# st.write("Datos unidos:")
# st.write(merged[['Departamento', 'Cantidad']])

# Crear el mapa de calor
# fig = px.choropleth(
#     merged,
#     geojson=peru_geojson.geometry,
#     locations='Departamento',
#     # featureidkey="properties.NOMBDEP",
#     color='Cantidad',
#     color_continuous_scale="Viridis",
#     # range_color=(0, merged['Cantidad'].max()),
#     labels={'Cantidad':'Cantidad de Egresos'},
#     title='Mapa de Calor de Egresos por Departamento'
# )
st.write("egresos_por_departamento:", egresos_por_departamento["Departamento"][2])
st.write("peru_geojson:", peru_geojson['NOMBDEP'][6])
# st.write("peru_geojson:", geojson["features"][0]["properties"])


fig = px.choropleth(
    egresos_por_departamento,
    geojson=peru_geojson.geometry,
    locations="Departamento",
    featureidkey="properties.NOMBDEP",
    color='Cantidad',
    color_continuous_scale="Viridis",
    labels={'Cantidad':'Cantidad de Egresos'},
    # title='Mapa de Perú'
)

fig.update_geos(
    fitbounds="locations",
    visible=False
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Mostrar el mapa
st.plotly_chart(fig)