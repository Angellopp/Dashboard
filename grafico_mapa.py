# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
import plotly.express as px
# from plotly.subplots import make_subplots

def grafico_mapa(merged, peru_geojson):
    custom_colorscale = [
        [0, "#ebeb34"],  # Púrpura oscuro con 70% de opacidad
        [0.1, "rgba(122, 227, 77, 0.80)"],  # Púrpura medio con 60% de opacidad
        [0.25, "rgba(39, 137, 129, 0.4)"],  # Azul con 50% de opacidad
        [0.5, "rgba(54, 92, 141, 0.5)"],  # Verde azulado con 40% de opacidad
        [0.75, "rgba(200, 179, 232, 0.60)"],  # Verde claro con 80% de opacidad
        [1, "rgba(208, 104, 235, 0.70)"]  # Amarillo brillante para los valores más altos
    ]

    # Crear el mapa coroplético
    fig = px.choropleth(
        merged,
        geojson=peru_geojson.geometry,
        locations=merged.index,
        color='Cantidad',
        color_continuous_scale=custom_colorscale,  # Aplicar escala de colores con opacidad
        labels={'Cantidad':'Cantidad de Egresos'},
    )

    fig.update_geos(
        fitbounds="locations",  # Ajusta el mapa para que se ajuste a las ubicaciones en los datos
        visible=False,
        projection_scale=5,  # Ajusta la escala del mapa para hacerlo más grande dentro del contenedor
        showcountries=False,
        countrycolor="black",
        showcoastlines=False,
        showland=False,
        landcolor="white",
        showframe=False
    )
    fig.update_layout(
        height=400,
        width=200,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # plot_bgcolor='red',  # Fondo del gráfico
        paper_bgcolor='white',  # Fondo del área de la gráfica
        font=dict(
            color='black'  # Color de las letras (texto)
        ),
        title_font=dict(
            color='black'  # Color de las letras del título
        ),
        coloraxis_colorbar=dict(
            title_font=dict(color='black'),
            tickfont=dict(color='black'),
            orientation='h',  # Cambia la orientación a horizontal
            x=0.5,  # Centra la barra horizontalmente
            xanchor='center',  # Alinea la barra en el centro
            y=-0.1,  # Mueve la barra hacia abajo
            len=0.9 ,  # Ajusta el largo de la barra de colores)
        )
    )
    return fig