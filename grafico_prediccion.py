import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pmdarima import auto_arima

def grafico_prediccion(df_ingresos, df_egresos, periods_to_forecast=12, capacity_limit=1000):
    # Convertir fechas a datetime
    df_ingresos['FECHA_INGRESO'] = pd.to_datetime(df_ingresos['FEC_FILIACION'], format='%Y%m%d')
    df_egresos['FECHA_EGRESO'] = pd.to_datetime(df_egresos['FECHA_EGRESO'], format='%Y%m%d')
    
    # Agrupar por fecha y contar ingresos y egresos
    ingresos_count = df_ingresos.groupby('FECHA_INGRESO').size().resample('ME').sum()
    egresos_count = df_egresos.groupby('FECHA_EGRESO').size().resample('ME').sum()
    
    # Asegurar que ambas series tienen el mismo índice
    date_range = pd.date_range(start=min(ingresos_count.index.min(), egresos_count.index.min()),
                               end=max(ingresos_count.index.max(), egresos_count.index.max()),
                               freq='ME')
    ingresos_count = ingresos_count.reindex(date_range, fill_value=0)
    egresos_count = egresos_count.reindex(date_range, fill_value=0)
    
    # Calcular el delta
    delta = ingresos_count - egresos_count
    
    # Intentar un modelo sin estacionalidad si falla el modelo estacional
    try:
        model = auto_arima(delta, seasonal=True, m=12, stepwise=True)
    except ValueError:
        model = auto_arima(delta, seasonal=False, stepwise=True)
    
    results = model.fit(delta)
    
    # Hacer la predicción
    forecast, conf_int = results.predict(n_periods=periods_to_forecast, return_conf_int=True)
    
    # Crear el rango de fechas para la predicción
    last_date = delta.index[-1]
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=periods_to_forecast, freq='ME')
    
    # Crear la figura
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        subplot_titles=("Ingresos y Egresos", "Delta y Predicción"))
    
    # Gráfico de Ingresos y Egresos
    fig.add_trace(go.Scatter(x=ingresos_count.index, y=ingresos_count, 
                             mode='lines', name='Ingresos', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=egresos_count.index, y=egresos_count, 
                             mode='lines', name='Egresos', line=dict(color='red')), row=1, col=1)
    
    # Gráfico de Delta y Predicción
    fig.add_trace(go.Scatter(x=delta.index, y=delta, mode='lines', 
                             name='Delta Real', line=dict(color='green')), row=2, col=1)
    fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode='lines', 
                             name='Predicción Delta', line=dict(color='orange', dash='dash')), row=2, col=1)
    
    # Añadir líneas de confianza y línea de límite de capacidad
    fig.add_trace(go.Scatter(x=future_dates, y=conf_int[:,0], mode='lines', 
                             line=dict(color='lightgrey'), showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=future_dates, y=conf_int[:,1], mode='lines', 
                             fill='tonexty', line=dict(color='lightgrey'), showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=future_dates, y=[capacity_limit] * len(future_dates), 
                             mode='lines', name='Capacidad del Hospital', line=dict(color='red', dash='dot')), row=2, col=1)
    
    # Actualizar el diseño
    fig.update_layout(height=800, title_text="Análisis de Ingresos, Egresos y Predicción de Delta")
    fig.update_xaxes(title_text="Fecha", row=2, col=1)
    fig.update_yaxes(title_text="Cantidad", row=1, col=1)
    fig.update_yaxes(title_text="Delta", row=2, col=1)
    
    return fig





#        1000   500
# 1000   -500  -1000
#        +500  -500  1000

