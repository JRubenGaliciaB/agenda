import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Visualización de Agenda", layout="wide", initial_sidebar_state="expanded")

# Estilos personalizados
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Datos simulados
ciudadanos_data = pd.DataFrame({
    "nombre": ["Juan Pérez", "María López", "Luis García", "Ana Martínez"],
    "disciplina": ["Música", "Danza", "Teatro", "Artes Visuales"],
    "municipio": ["Querétaro", "San Juan del Río", "El Marqués", "Corregidora"]
})

eventos_data = pd.DataFrame({
    "actividad": ["Concierto de Rock", "Presentación de Ballet", "Obra de Teatro", "Exposición de Arte"],
    "municipio": ["Querétaro", "San Juan del Río", "El Marqués", "Corregidora"]
})

# Espacio superior para la foto de perfil y el nombre
# col1, col2 = st.columns([1, 4])
# with col1:
#    st.image("foto_perfil.jpg", width=150)
# with col2:
#    st.markdown("## Nombre del Servidor Público")

# KPIs principales
st.markdown("### Indicadores Principales")
col1, col2 = st.columns(2)
with col1:
    st.metric("Ciudadanos Atendidos", len(ciudadanos_data))
    st.metric("Municipios Visitados", ciudadanos_data['municipio'].nunique())
with col2:
    st.metric("Actividades Realizadas", len(eventos_data))

# Detalle de ciudadanos atendidos
st.markdown("### Ciudadanos Atendidos")
disciplina = st.selectbox("Filtrar por disciplina", ["Todas"] + list(ciudadanos_data["disciplina"].unique()))
if disciplina != "Todas":
    ciudadanos_data = ciudadanos_data[ciudadanos_data["disciplina"] == disciplina]
st.dataframe(ciudadanos_data)

# Detalle de eventos
st.markdown("### Eventos Realizados")
eventos_por_municipio = eventos_data["municipio"].value_counts().reset_index()
eventos_por_municipio.columns = ["Municipio", "Número de Eventos"]
fig = px.bar(
    eventos_por_municipio,
    x="Municipio",
    y="Número de Eventos",
    title="Número de Eventos por Municipio",
    labels={"Número de Eventos": "Eventos", "Municipio": "Municipio"},
    template="plotly_dark",
)
st.plotly_chart(fig, use_container_width=True)
