import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from grafico_mapa import grafico_mapa
from grafico_hombres_vs_mujeres import grafico_hombres_vs_mujeres
from grafico_edad_sexo import grafico_edad_sexo
from grafico_circular_por_distrito import grafico_circular_por_distrito
from grafico_prediccion import grafico_prediccion

# set page config para la configuracion de la pagina
st.set_page_config(
    page_title="Dashboard",
    page_icon="🏠",
    layout="wide",
    # initial_sidebar_state="expanded",
)
##
# CSS para personalizar el estilo del botón home
st.markdown(
    """
    <style>
    .pink-button {
        color: white !important;               /* color del texto */
        padding: 5px 10px;        /* padding */
        font-size: 20px;           /* tamaño de la fuente */
        text-align: center;        /* centrar el texto */
        display: inline-block;     /* mostrar como bloque en línea */
        border-radius: 27px;
        width: -webkit-fill-available;
        background: #B5904F;
        box-shadow: inset 1px 4px 12px 7px rgba(0, 0, 0, 0.25);
        border-color: #B5904F;
        text-decoration: none;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar con opciones
with st.sidebar:
    # st.title("Home")
    st.markdown('<a href="https://portal.inen.sld.pe/" target="_blank" class="pink-button">🏠  Home</a>', unsafe_allow_html=True)
    # st.write("Esta es la página principal.")

    # st.title("Dashboard")
    # st.write("Aquí puedes ver los gráficos e informes del Dashboard.")
    selected_year = st.selectbox("Tipo", ["Graficos", "Tablas"], index=1)


    # st.title("Año")
    # st.write("Aquí puedes seleccionar el año de análisis.")
    selected_year = st.selectbox("Año", [2022, 2023, 2024], index=2)
    # st.write(f"Has seleccionado el año: {selected_year}")


mes_dict = {
    "TODOS": None,  # Opción para seleccionar todos los meses
    "ENERO": "01",
    "FEBRERO": "02",
    "MARZO": "03",
    "ABRIL": "04",
    "MAYO": "05",
    "JUNIO": "06",
    "JULIO": "07",
    "AGOSTO": "08",
    "SEPTIEMBRE": "09",
    "OCTUBRE": "10",
    "NOVIEMBRE": "11",
    "DICIEMBRE": "12"
}

departamentos = ["TODOS"] + [
    "AMAZONAS", "ANCASH", "APURIMAC", "AREQUIPA", "AYACUCHO", "CAJAMARCA", 
    "CALLAO", "CUSCO", "HUANCAVELICA", "HUANUCO", "ICA", "JUNIN", 
    "LA LIBERTAD", "LAMBAYEQUE", "LIMA", "LORETO", "MADRE DE DIOS", 
    "MOQUEGUA", "PASCO", "PIURA", "PUNO", "SAN MARTIN", "TACNA", 
    "TUMBES", "UCAYALI"
]

macroregiones = {
    "NORTE": ["CAJAMARCA", "LA LIBERTAD", "LAMBAYEQUE", "PIURA", "TUMBES"],
    "SUR": ["AREQUIPA", "CUSCO", "MADRE DE DIOS", "MOQUEGUA", "PUNO", "TACNA"],
    "CENTRO": ["ANCASH", "AYACUCHO", "HUANCAVELICA", "HUANUCO", "ICA", "JUNIN", "LIMA", "PASCO"],
    "LIMA": ["LIMA", "CALLAO"],
    "ORIENTE": ["AMAZONAS", "LORETO", "SAN MARTÍN", "UCAYALI"]
}

provincias_por_departamento = {
    "AMAZONAS": ["CHACHAPOYAS", "BAGUA", "BONGARÁ", "CONDORCANQUI", "LUYA", "RODRIGUEZ DE MENDOZA", "UTCUBAMBA"],
    "ANCASH": ["HUARAZ", "AIJA", "ANTONIO RAIMONDI", "ASUNCION", "BOLOGNESI", "CARHUAZ", "CARLOS F. FITZC", "CASMA", "CORONGO", "HUARI", "HUARMEY", "HUAYLAS", "MARISCAL LUZURIAGA", "OCROS", "PALLASCA", "POMABAMBA", "RECUAY", "SANTA", "SIHUAS", "YUNGAY"],
    "APURIMAC": ["ABANCAY", "ANDAHUAYLAS", "ANTABAMBA", "AYMARAES", "COTABAMBAS", "CHINCHEROS", "GRAU"],
    "AREQUIPA": ["AREQUIPA", "CAMANA", "CARAVELI", "CASTILLA", "CAYLLOMA", "CONDESUYOS", "ISLAY", "LA UNION"],
    "AYACUCHO": ["HUAMANGA", "CANGALLO", "HUANCA SANCOS", "HUANTA", "LA MAR", "LUCANAS", "PARINACOCHAS", "PAUCAR DEL SARA SARA", "SUCRE", "VICTOR FAJARDO", "VILCAS HUAMAN"],
    "CAJAMARCA": ["CAJAMARCA", "CAJABAMBA", "CELENDIN", "CHOTA", "CONTUMAZÁ", "CUTERVO", "HUALGAYOC", "JAÉN", "SAN IGNACIO", "SAN MARCOS", "SAN MIGUEL", "SAN PABLO", "SANTA CRUZ"],
    "CALLAO": ["CALLAO"],
    "CUSCO": ["CUSCO", "ACOMAYO", "ANTA", "CALCA", "CANAS", "CANCHIS", "CHUMBIVILCAS", "ESPINAR", "LA CONVENCION", "PARURO", "PAUCARTAMBO", "QUISPICANCHI", "URUBAMBA"],
    "HUANCAVELICA": ["HUANCAVELICA", "ACOBAMBA", "ANGARAES", "CASTROVIRREYNA", "CHURCAMPA", "HUAYTARA", "TAYACAJA"],
    "HUANUCO": ["HUÁNUCO", "AMBO", "DOS DE MAYO", "HUACAYBAMBA", "HUAMALÍES", "LEONCIO PRADO", "MARAÑON", "PACHITEA", "PUERTO INCA", "LAURICOCHA", "YAROWILCA"],
    "ICA": ["ICA", "CHINCHA", "NASCA", "PALPA", "PISCO"],
    "JUNIN": ["HUANCAYO", "CHANCHAMAYO", "CONCEPCIÓN", "JAUJA", "JUNÍN", "SATIPO", "TARMA", "YAULI", "CHUPACA"],
    "LA LIBERTAD": ["TRUJILLO", "ASCOPE", "BOLÍVAR", "CHEPÉN", "GRAN CHIMÚ", "JULCÁN", "OTUZCO", "PACASMAYO", "PATAZ", "SÁNCHEZ CARRIÓN", "SANTIAGO DE CHUCO", "VIRÚ"],
    "LAMBAYEQUE": ["CHICLAYO", "FERREÑAFE", "LAMBAYEQUE"],
    "LIMA": ["LIMA", "BARRANCA", "CAÑETE", "CANTA", "CAJATAMBO", "HUARAL", "HUAROCHIRI", "HUAURA", "OYÓN", "YAUYOS"],
    "LORETO": ["MAYNAS", "ALTO AMAZONAS", "LORETO", "MARISCAL RAMÓN CASTILLA", "REQUENA", "UCAYALI", "DATEM DEL MARAÑÓN", "PUTUMAYO"],
    "MADRE DE DIOS": ["TAMBOPATA", "MANU", "TAHUAMANU"],
    "MOQUEGUA": ["MARISCAL NIETO", "GENERAL SÁNCHEZ CERRO", "ILO"],
    "PASCO": ["PASCO", "DANIEL ALCIDES CARRIÓN", "OXAPAMPA"],
    "PIURA": ["PIURA", "AYABACA", "HUANCABAMBA", "MORROPÓN", "PAITA", "SULLANA", "TALARA", "SECHURA"],
    "PUNO": ["PUNO", "AZÁNGARO", "CARABAYA", "CHUCUITO", "EL COLLAO", "HUANCANÉ", "LAMPA", "MELGAR", "MOHO", "SAN ANTONIO DE PUTINA", "SAN ROMÁN", "SANDIA", "YUNGUYO"],
    "SAN MARTIN": ["MOYOBAMBA", "BELLAVISTA", "EL DORADO", "HUALLAGA", "LAMAS", "MARISCAL CÁCERES", "PICOTA", "RIOJA", "SAN MARTÍN", "TOCACHE"],
    "TACNA": ["TACNA", "CANDARAVE", "JORGE BASADRE", "TARATA"],
    "TUMBES": ["TUMBES", "CONTRALMIRANTE VILLAR", "ZARUMILLA"],
    "UCAYALI": ["CORONEL PORTILLO", "ATALAYA", "PADRE ABAD", "PURÚS"],
}

#funcion para obtener departamentos por macroregion
def obtener_departamentos_por_macroregion(selected_macroregion):
    if selected_macroregion == "TODOS":
        return departamentos
    else:
        return ["TODOS"] + macroregiones.get(selected_macroregion, [])
#funcion para obtener provincias por departamento
def obtener_provincias_por_departamento(selected_departamento):
    if selected_departamento == "TODOS":
        return ["TODOS"]
    else:
        return ["TODOS"] + provincias_por_departamento.get(selected_departamento, [])

    
# Estilo personalizado para la página
page_bg = """
<style>
    [data-testid="stAppViewContainer"]{
        background-color: #FFFFFF;
        color: black;
    }
    [data-testid="stHeader"]{
        background-color: #002265;
        color: white;
        height: 70px;
    }
    [data-testid="stSidebarContent"]{
        background: #002265;
    }
    [data-testid="stAppViewBlockContainer"]{
        background-color: #002265;
        padding: 4rem 1rem 2rem;
    }
    [data-testid="stHorizontalBlock"]{
        color: white;
    }
    div[data-baseweb="select"] > div {
        border-radius: 20px;
        background: #B5904F;
        box-shadow: inset 1px 4px 12px 7px rgba(0, 0, 0, 0.25);
        border-color: #B5904F;
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Encabezado
image_path = "logoinen.svg"
headerr = st.container()
with headerr:
    col1, col2, col3 = st.columns([0.5, 1, 1], vertical_alignment="center")
    
    with col1:
        lef,middle,right=st.columns([1,2,1], vertical_alignment="center")
        with middle:
            st.image(image_path, width=200, use_column_width=True)
    with col2:
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%; font-size: 120px;">
                <h2 style="color: white; text-align: center; font-weight: bold">Análisis Integral de Ingresos Hospitalarios y Egresos en Perú</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        left, middle, right1,right2 = st.columns(4, vertical_alignment="bottom")
        selected_mes = left.selectbox("MES", list(mes_dict.keys()))
        selected_macroregion = middle.selectbox("MACROREGION", ["TODOS", "NORTE", "SUR", "CENTRO", "ORIENTE", "LIMA"])
        selected_departamento = right1.selectbox( "DEPARTAMENTO",  obtener_departamentos_por_macroregion(selected_macroregion))
        selected_provincia = right2.selectbox("PROVINCIA", obtener_provincias_por_departamento(selected_departamento))
 
# Estilo para contenedores
container_style = lambda height: f"""
    <div style="background-color: white; box-shadow: 0px 4px 8px 2px rgba(0, 0, 0, 0.25);
    height: {height}px; padding: 10px; border-radius: 20px; margin-bottom: 9px"></div>
"""
container_style_2 = lambda height: f"""
    <div style="
        box-shadow: inset 0px 4px 8px 2px rgba(0, 0, 0, 0.25), 0px 4px 8px 2px rgba(0, 0, 0, 0.25);
        height: {height}px; 
        padding: 10px;
        margin-bottom: 9px;
        border-radius: 20px;
        background: #D5EBFF;
    "></div>
"""

# Cargar datos
# URL del archivo GeoJSON de los departamentos de Perú
geojson_url = 'https://raw.githubusercontent.com/juaneladio/peru-geojson/master/peru_departamental_simple.geojson'
# url_csv_egresos = './data/ingresos/Listado_pacientes_nuevos_inen_enero2022_junio2024.csv'
# url_csv_ingresos = './data/ingresos/Listado_pacientes_nuevos_inen_enero2022_junio2024.csv'
url_csv_egresos = 'Listado_egresos_hopitalizados_enero_2022_junio2024.csv'
url_csv_ingresos = 'Listado_pacientes_nuevos_inen_enero2022_junio2024.csv'

peru_geojson = gpd.read_file(geojson_url)
df_i = pd.read_csv(url_csv_ingresos, encoding='latin-1')
df_e = pd.read_csv(url_csv_egresos, encoding='latin-1')
df_i_totales = pd.read_csv(url_csv_ingresos, encoding='latin-1')
df_e_totales = pd.read_csv(url_csv_egresos, encoding='latin-1')

# Extraer el departamento de la columna LUGAR_RESIDENCIA
df_i['DEPARTAMENTO'] = df_i['LUGAR_RESIDENCIA'].str.split('-').str[0].str.strip().str.upper()
df_i['PROVINCIA'] = df_i['LUGAR_RESIDENCIA'].str.split('-').str[1].str.strip().str.upper()
# print(df_i['PROVINCIA'])
###### FILTROS ######

# Filtrar los datos por el año seleccionado
df_i['AÑO_FILIACION'] = df_i['FEC_FILIACION'].astype(str).str[:4]  # Extraer el año de FECHA_EGRESO
df_i = df_i[df_i['AÑO_FILIACION'] == str(selected_year)]

# Filtrar departamentos según la macroregión seleccionada
if selected_macroregion != "TODOS":
    departamentos_en_macroregion = macroregiones.get(selected_macroregion, [])
    df_i = df_i[df_i['DEPARTAMENTO'].isin(departamentos_en_macroregion)]

# Filtrar los datos por el mes seleccionado si no es "Todos"
if mes_dict[selected_mes] is not None:
    df_i['MES_FILIACION'] = df_i['FEC_FILIACION'].astype(str).str[4:6]  # Extraer el mes de FECHA_EGRESO
    df_i = df_i[df_i['MES_FILIACION'] == mes_dict[selected_mes]]

# Filtrar los datos por el departamento seleccionado si no es "Todos"
if selected_departamento != "TODOS":
    df_i = df_i[df_i['DEPARTAMENTO'] == selected_departamento]

if selected_provincia != "TODOS":
    df_i = df_i[df_i['PROVINCIA'] == selected_provincia]
    
# Si está vacío, recargar el conjunto de datos completo sin aplicar filtros
if df_i.empty:
    df_i = pd.read_csv(url_csv_egresos, encoding='latin-1')



# Contar la cantidad de egresos por departamento
if 'DEPARTAMENTO'  not in df_i.columns or 'PROVINCIA' not in df_i.columns:
    st.warning("No hay datos disponibles para mostrar en el mapa. Verifique los filtros seleccionados.")
    df_i = pd.read_csv(url_csv_egresos, encoding='latin-1')
    df_i['DEPARTAMENTO'] = df_i['LUGAR_RESIDENCIA'].str.split('-').str[0].str.strip().str.upper()
    df_i['PROVINCIA'] = df_i['LUGAR_RESIDENCIA'].str.split('-').str[1].str.strip().str.upper()
    # df_i = pd.read_csv(url_csv_egresos, encoding='latin-1')

# if 'PROVINCIA' not in df_i.columns:
    # st.warning("No hay datos disponibles para mostrar en el mapa. Verifique los filtros seleccionados.")

# Cálculo de estadísticas
total_patients = len(df_i)
male_patients = len(df_i[df_i['SEXO'] == 'MASCULINO'])
female_patients = len(df_i[df_i['SEXO'] == 'FEMENINO'])
male_percentage = (male_patients / total_patients) * 100
female_percentage = (female_patients / total_patients) * 100

egresos_por_departamento = df_i['DEPARTAMENTO'].value_counts().reset_index()
egresos_por_departamento.columns = ['Departamento', 'Cantidad']

egresos_por_provincia = df_i['PROVINCIA'].value_counts().reset_index()
egresos_por_provincia.columns = ['Provincia', 'Cantidad']

# print(df_i)
# Unir los datos de los egresos con el GeoJSON
peru_geojson['Departamento'] = peru_geojson['NOMBDEP'].str.strip().str.upper()
merged = peru_geojson.merge(egresos_por_departamento, on='Departamento', how='left')

fig = grafico_mapa(merged, peru_geojson)

# Contenedores
contiene1, contiene2, contiene3 = st.columns([0.6, 1, 0.8], vertical_alignment="bottom")
with contiene1:
    # st.markdown(container_style(50), unsafe_allow_html=True)
    with st.container():
        #barra de progreso 
        st.markdown(
            """
            <style>
            .progress-bar-container {
                width: 100%;
                background-color: #f3f3f3;
                border-radius: 25px;
                padding: 3px;
                margin: 10px 0;
            }

            .progress-bar {
                background-color: #8986ef;
                height: 86px;
                border-radius: 25px;
                text-align: center;
                color: white;
                line-height: 30px;
                font-weight: bold;
                display: block;
                justify-items: center;
                align-content: center;
                padding-top: 5px;
                        }
            </style>
            """, unsafe_allow_html=True
        )
        progress_placeholder = st.empty()
        # button_clicked = st.button("Rerun")
        for percent_complete in range(101):
            progress_text = f"{percent_complete}%"
            progress_bar_html = f"""
            <div class="progress-bar-container">
                 <div class="progress-bar" style="width: {percent_complete}%; font-size: 5vh; ">
                    {progress_text}
                    <span style="font-size: 2vh; display: block;">Capacidad</span>
                </div>
            </div>
            """
            progress_placeholder.markdown(progress_bar_html, unsafe_allow_html=True)
            # time.sleep(0.05)
        st.plotly_chart(fig, use_container_width=True)

with contiene2:
    # Custom CSS para mujeres vs hombre
    css = """
    <style>
        .container {
           background-color: white;
            border-radius: 15px;
            padding-bottom: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            margin-bottom: 12px;
            display: flex;
            flex-direction: column;
        }
        .header {
            color: navy;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .subheader {
            color: navy;
            font-size: 18px;
            text-align: center;
            margin-bottom: 20px;
        }
        .stats {
            display: flex;
            justify-content: space-around;
            align-items: center;
        }
        .stat {
            text-align: center;
        }
        .male-icon {
            color: #ADD8E6;
            font-size: 40px;
        }
        .female-icon {
            color: #FFC0CB;
            font-size: 40px;
        }
        .percentage {
            font-size: 36px;
            font-weight: bold;
        }
        .male-percentage {
            color: #0000FF;
        }
        .female-percentage {
            color: #800080;
        }
        .count {
            font-size: 14px;
        }
        .label {
            font-size: 14px;
        }
    </style>
    """
    # Add custom CSS
    st.markdown(css, unsafe_allow_html=True)

    # mujeresvshombre   
    grafico2 = grafico_hombres_vs_mujeres(total_patients, male_percentage, male_patients, female_percentage, female_patients)
    st.markdown(grafico2, unsafe_allow_html=True)
    #graifca de barras por sexo de los pacientes
    grafico3 = grafico_edad_sexo(df_i)
    st.plotly_chart(grafico3, use_container_width=True)
    # st.markdown(container_style(295), unsafe_allow_html=True)

with contiene3:
    # st.markdown(container_style(250), unsafe_allow_html=True)
    # Crear subparcelas: usar el tipo 'dominio' para la subparcela circular 
    grafico4 = grafico_circular_por_distrito(df_i)
    st.plotly_chart(grafico4, use_container_width=True)
    grafico5 = grafico_prediccion(df_i_totales, df_e_totales)
    st.plotly_chart(grafico5, use_container_width=True)
    # st.markdown(container_style(290), unsafe_allow_html=True)
    
    

    