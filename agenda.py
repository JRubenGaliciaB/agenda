import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos desde un archivo Excel
def cargar_datos():
    return pd.read_excel("datos_actividades.xlsx")

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

# Cargar datos
datos = cargar_datos()

# Espacio superior para la foto de perfil y el nombre
col1, col2 = st.columns([1, 4])
with col1:
    st.image("foto_perfil.jpg", width=150)
with col2:
    st.markdown("## Nombre del Servidor Público")

# Menú desplegable para seleccionar el rango de tiempo
st.sidebar.header("Filtrar por tiempo")
rango_tiempo = st.sidebar.selectbox(
    "Selecciona el rango de tiempo",
    ["Total", "Mensual", "Anual", "Periodo personalizado"],
)

if rango_tiempo == "Periodo personalizado":
    fecha_inicio = st.sidebar.date_input("Fecha de inicio")
    fecha_fin = st.sidebar.date_input("Fecha de fin")
    datos = datos[(datos['fecha'] >= fecha_inicio) & (datos['fecha'] <= fecha_fin)]
elif rango_tiempo == "Mensual":
    mes = st.sidebar.selectbox("Selecciona el mes", datos['mes'].unique())
    datos = datos[datos['mes'] == mes]
elif rango_tiempo == "Anual":
    anio = st.sidebar.selectbox("Selecciona el año", datos['anio'].unique())
    datos = datos[datos['anio'] == anio]

# KPIs principales
st.markdown("### Indicadores Principales")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ciudadanos Atendidos", datos['ciudadanos_atendidos'].sum())
with col2:
    st.metric("Municipios Visitados", datos['municipios_visitados'].nunique())
with col3:
    st.metric("Actividades con Medios", datos['actividades_medios'].sum())

# Menús desplegables para disciplinas
st.markdown("### Detalle por Disciplina Artística o Cultural")
disciplina = st.selectbox("Selecciona la disciplina", datos['disciplina'].unique())
filtered_data = datos[datos['disciplina'] == disciplina]

# Gráficos de detalle
st.markdown("#### Detalle de Actividades")
grafico = px.bar(
    filtered_data,
    x="actividad",
    y="ciudadanos_atendidos",
    title=f"Actividades en la disciplina: {disciplina}",
    labels={"ciudadanos_atendidos": "Ciudadanos Atendidos", "actividad": "Actividad"},
    template="plotly_dark",
)
st.plotly_chart(grafico, use_container_width=True)

# Guardar los datos procesados en un botón de descarga
@st.cache_data
def convertir_csv(df):
    return df.to_csv(index=False).encode('utf-8')

data_csv = convertir_csv(filtered_data)
st.download_button(
    label="Descargar datos filtrados",
    data=data_csv,
    file_name="datos_filtrados.csv",
    mime="text/csv",
)
