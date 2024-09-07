import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA

def grafico_prediccion(df_egresos):
    # Convertir FECHA_INGRESO y FECHA_EGRESO a formato datetime
    df_egresos['FECHA_INGRESO'] = pd.to_datetime(df_egresos['FECHA_INGRESO'], format='%Y%m%d')
    df_egresos['FECHA_EGRESO'] = pd.to_datetime(df_egresos['FECHA_EGRESO'], format='%Y%m%d')

    # Crear una serie temporal mensual con el número de ingresos por mes
    df_egresos.set_index('FECHA_INGRESO', inplace=True)
    serie_temporal = df_egresos.resample('ME').size()
    
    # Dividir los datos en entrenamiento y prueba
    train_size = int(len(serie_temporal) * 0.8)
    train, test = serie_temporal[:train_size], serie_temporal[train_size:]

    # Ajustar el modelo ARIMA
    modelo = ARIMA(train, order=(5, 1, 0))
    modelo_fit = modelo.fit()

    # Realizar predicciones
    predicciones = modelo_fit.forecast(steps=len(test))
    predicciones = pd.Series(predicciones, index=test.index)

    # Crear gráfico con las predicciones
    fig = go.Figure()

    # Agregar la serie temporal real
    fig.add_trace(go.Scatter(
        x=serie_temporal.index,
        y=serie_temporal.values,
        mode='lines',
        name='Datos Reales',
        line=dict(color='blue')
    ))

    # Agregar las predicciones
    fig.add_trace(go.Scatter(
        x=predicciones.index,
        y=predicciones.values,
        mode='lines',
        name='Predicciones',
        line=dict(color='red', dash='dash')
    ))

    # Actualizar el diseño del gráfico
    fig.update_layout(
        title=dict(
            text='Predicción de Demanda Hospitalaria',
            font=dict(color='black')
        ),
        xaxis_title=dict(
            text="Fecha",
            font=dict(color='black')
        ),
        yaxis_title=dict(
            text="Número de Pacientes",
            font=dict(color='black')
        ),
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black'),
    )

    # Actualizar el diseño del eje
    fig.update_xaxes(
        tickfont=dict(size=12, color='black'),
        showgrid=True, gridwidth=1, gridcolor='lightgrey'
    )
    fig.update_yaxes(
        tickfont=dict(size=12, color='black'),
        showgrid=True, gridwidth=1, gridcolor='lightgrey'
    )
    
    return fig
