import pandas as pd
import streamlit as st
import plotly.express as px
from connection_VE import MySQLConnection
from streamlit_autorefresh import st_autorefresh

# Configurar la página de Streamlit
st.set_page_config(page_title="Producción Energética", page_icon="⚡", layout="wide")

# Crear conexión con la base de datos
conexion = MySQLConnection()

# Título
st.title("📊 Producción Energética")

# Inicializar el estado de sesión para los filtros
if "filtros" not in st.session_state:
    st.session_state.filtros = {
        "analizadores": None,
        "fecha_inicio": None,
        "fecha_fin": None
    }

# Función para resetear los filtros
def reset_filters():
    st.session_state.filtros = {
        "analizadores": None,
        "fecha_inicio": df["fecha"].min(),
        "fecha_fin": df["fecha"].max()
    }

try:
    # Obtener una sesión desde el pool de conexiones
    session = conexion.obtener_sesion()

    # Consulta SQL
    consulta_sql = "SELECT * FROM produccion_anp;"
    df = pd.read_sql(consulta_sql, session.connection())

    # Convertir la columna 'fecha' a datetime
    df["fecha"] = pd.to_datetime(df["fecha"], format='%Y-%m-%d %H:%M:%S.%f')

    # Obtener rango de fechas
    start_date = df["fecha"].min()
    end_date = df["fecha"].max()

    # Barra lateral para filtros
    st.sidebar.header("Filtros")

    # Botón para resetear los filtros
    if st.sidebar.button("Resetear Filtros"):
        reset_filters()

    # Filtro de analizadores
    analizadores = st.sidebar.multiselect(
        "Selecciona el analizador",
        df["analizador"].unique(),
        default=st.session_state.filtros["analizadores"]
    )

    # Filtro de fechas
    fecha_inicio = st.sidebar.date_input(
        "Fecha de inicio",
        value=st.session_state.filtros["fecha_inicio"] or start_date,
        min_value=start_date,
        max_value=end_date
    )
    fecha_fin = st.sidebar.date_input(
        "Fecha de fin",
        value=st.session_state.filtros["fecha_fin"] or end_date,
        min_value=start_date,
        max_value=end_date
    )

    # Actualizar el estado de sesión con los valores seleccionados
    st.session_state.filtros = {
        "analizadores": analizadores,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    }

    # Convertir fechas seleccionadas a datetime
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Aplicar filtros
    df_filtrado = df[(df["fecha"] >= fecha_inicio) & (df["fecha"] <= fecha_fin)]
    if analizadores:
        df_filtrado = df_filtrado[df_filtrado["analizador"].isin(analizadores)]

    # Mostrar tabla de datos filtrados
    #st.subheader("📋 Datos Filtrados")
    #st.dataframe(df_filtrado)

    # Graficar datos
    if not df_filtrado.empty:
        st.subheader("📈 Producción energética en el tiempo")
        fig = px.line(
            df_filtrado,
            x="fecha",
            y="producción",
            color="analizador",
            title="Producción de Energía por Analizador",
            labels={"fecha": "Fecha", "producción": "Producción Energética [W]", "analizador": "Analizador"},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔹 Producción energética total por analizador")
        fig_bar = px.bar(
            df_filtrado,
            x="analizador",
            y="producción",
            color="analizador",
            title="Producción de Energía por Analizador",
            labels={"producción": "Producción Energética [W]", "analizador": "Analizador"},
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No hay datos para mostrar con los filtros seleccionados.")

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")

finally:
    # Cerrar la sesión después de usarla
    if 'session' in locals():
        conexion.cerrar_sesion(session)

# Recargar cada tantos segundos
#st_autorefresh(interval=10 * 1000, key="data_refresh")