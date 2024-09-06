import plotly.graph_objects as go

def grafico_edad_sexo(df):
    # Definir los rangos de edad
    age_ranges = [
        (0, 14, '[00 - 14]'),
        (15, 19, '[15 - 19]'),
        (20, 34, '[20 - 34]'),
        (35, 44, '[35 - 44]'),
        (45, 64, '[45 - 64]'),
        (65, 150, '[65+]')
    ]

    # Función para asignar rango de edad
    def assign_age_range(age):
        for start, end, label in age_ranges:
            if start <= age <= end:
                return label
        return 'Unknown'

    # Asumiendo que tienes una columna 'EDAD' en tu DataFrame
    df['AGE_RANGE'] = df['EDAD'].apply(assign_age_range)

    # Crear el DataFrame para la gráfica
    gender_age_counts = df.groupby(['AGE_RANGE', 'SEXO']).size().unstack(fill_value=0)
    gender_age_counts = gender_age_counts.reindex([range_label for _, _, range_label in age_ranges[::-1]])

    # Crear la figura
    fig = go.Figure()

    # Agregar barras para mujeres (valores negativos para que aparezcan a la izquierda)
    fig.add_trace(go.Bar(
        y=gender_age_counts.index,
        x=-gender_age_counts['FEMENINO'],
        name='Femenino',
        orientation='h',
        marker_color='purple',
        text=gender_age_counts['FEMENINO'],  # Mostrar valores de las mujeres
        textposition='outside',  # Posición del texto fuera de la barra
        insidetextanchor='start',  # Anclar texto al inicio
        texttemplate='%{text}',  # Formato del texto
        cliponaxis=False,  # Permitir que el texto se salga del área de la gráfica
        textfont=dict(color='black', size=12)  # Color y tamaño de la letra
    ))

    # Agregar barras para hombres
    fig.add_trace(go.Bar(
        y=gender_age_counts.index,
        x=gender_age_counts['MASCULINO'],
        name='Masculino',
        orientation='h',
        marker_color='teal',
        text=gender_age_counts['MASCULINO'],  # Mostrar valores de los hombres
        textposition='outside',  # Posición del texto fuera de la barra
        insidetextanchor='start',  # Anclar texto al inicio
        texttemplate='%{text}',  # Formato del texto
        cliponaxis=False,  # Permitir que el texto se salga del área de la gráfica
        textfont=dict(color='black', size=12)  # Color y tamaño de la letra

    ))

    # Configurar el diseño
    fig.update_layout(
        barmode='relative',
        bargap=0.1,
        title=dict(
            text='Distribución por Edad y Género',
            font=dict(color='black')  # Color del título
        ),
        xaxis=dict(
            title='Cantidad',
            tickvals=[-400, -300, -200, -100, 0, 100, 200, 300, 400],
            ticktext=['400', '300', '200', '100', '0', '100', '200', '300', '400'],
            title_standoff=15,  # Espacio entre el título y el eje
            color='green',  # Color de los valores del eje x
            titlefont=dict(color='black', size=12),  # Color del título del eje x
            tickfont=dict(color='black', size=12),  # Color de las etiquetas del eje x
            tickangle=0  # Orientación horizontal de las etiquetas

        ),
        yaxis=dict(
            title='Rango de Edad',
            color='green',  # Color de los valores del eje y
            titlefont=dict(color='black', size=12),  # Color del título del eje y
            tickfont=dict(color='black', size=12)  # Color de las etiquetas del eje y

        ),
        legend=dict(
            x=0.35, y=1.05, orientation='h',
            font=dict(color='black')  # Color de la leyenda
        ),
        showlegend=True,
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor='white',  # Fondo del gráfico blanco
        paper_bgcolor='white'  # Fondo del papel (todo el área) blanco
    )

    return fig

