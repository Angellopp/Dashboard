import plotly.express as px
def grafico_circular_por_distrito(df_e):

    data = dict(
        character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
        value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

    fig = px.sunburst(
        data,
        names='character',
        parents='parent',
        values='value',
    )
     # Ajustar el tamaño del gráfico
    fig.update_layout(
        height=300,  # Aumenta la altura del gráfico
        width=500,   # Aumenta el ancho del gráfico
        paper_bgcolor='white',  # Fondo del Ã¡rea de la grÃ¡fica
        margin=dict(l=0, r=0, t=0, b=0)  # Ajusta los márgenes si es necesario
    )
    
    # Aumentar la escala del gráfico dentro de la figura
    fig.update_traces(
        textinfo="label+value+percent parent",  # Mostrar más información en el gráfico
        # hoverinfo="label+value+percent parent",  # Mostrar en el hover
        marker=dict(line=dict(width=2))  # Ajusta el borde de los sectores
    )
    # figs.show()
    return fig
