import pandas as pd
import plotly.graph_objects as go

def grafico_barras(df_egresos):
    # Convertir FECHA_INGRESO y FECHA_EGRESO a formato datetime
    df_egresos['FECHA_INGRESO'] = pd.to_datetime(df_egresos['FECHA_INGRESO'], format='%Y%m%d')
    df_egresos['FECHA_EGRESO'] = pd.to_datetime(df_egresos['FECHA_EGRESO'], format='%Y%m%d')
    
    # Calcular el tiempo de hospitalización (días entre FECHA_INGRESO y FECHA_EGRESO)
    df_egresos['TIEMPO_HOSPITALIZACION'] = (df_egresos['FECHA_EGRESO'] - df_egresos['FECHA_INGRESO']).dt.days
    # max_hospitalizacion = df_egresos['TIEMPO_HOSPITALIZACION'].max()
    
    # Definir intervalos personalizados con np.inf para el rango más alto
    bins = [0, 7, 14, 30, 60, 120, 180, 227]  # Usar np.inf para el rango final
    etiquetas = ["0-7 días", "8-14 días", "15-30 días", "31-60 días", 
                 "61-120 días", "121-180 días", "181-227 días"]
    
    # Calcular las frecuencias para cada intervalo
    df_egresos['GRUPO_TIEMPO'] = pd.cut(df_egresos['TIEMPO_HOSPITALIZACION'], bins=bins, labels=etiquetas, right=False)
    frecuencias = df_egresos['GRUPO_TIEMPO'].value_counts(sort=False)
    
    # Crear un gráfico de barras con las frecuencias
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=frecuencias.index,  # Intervalos de días
        y=frecuencias.values,  # Frecuencias
        name='Frecuencia',
        marker=dict(color='#4C95D9')
    ))

    # Actualizar el diseño del gráfico
    fig.update_layout(
        title=dict(
            text='Frecuencia de Tiempos de Hospitalización',
            font=dict(color='black')
        ),
        xaxis_title=dict(
            text="Intervalo de Tiempo de Hospitalización (días)",
            font=dict(color='black')
        ),
        yaxis_title=dict(
            text="Número de Pacientes",
            font=dict(color='black')
        ),
        height=600,
        plot_bgcolor='white',  # Fondo blanco
        paper_bgcolor='white',  # Fondo blanco para el gráfico completo
        font=dict(color='black'),  # Letras negras
        xaxis_tickangle=-45,  # Girar las etiquetas del eje X
    )

    # Mejorar la visibilidad de las etiquetas del eje X
    fig.update_xaxes(
        tickfont=dict(size=12, color='black'),  # Ajuste del tamaño y color de las etiquetas
        showgrid=True, gridwidth=1, gridcolor='lightgrey'
    )
    
    # Mejorar la visibilidad de las etiquetas del eje Y
    fig.update_yaxes(
        tickfont=dict(size=12, color='black'),  # Ajuste del tamaño y color de las etiquetas
        showgrid=True, gridwidth=1, gridcolor='lightgrey'
    )

    return fig