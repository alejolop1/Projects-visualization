from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from DB_connection import MySQLConnection

st.set_page_config(page_title="Dashboard GIMEL", page_icon=":bar_chart:", layout="wide")



# Crear una instancia de la conexión con el archivo JSON de credenciales
conexion = MySQLConnection("home/documentos/workspace/config/credenciales.json")

# Título de la aplicación Streamlit
st.title("Visualización de Producción Energética de los paneles")

# Conectar a la base de datos
engine = conexion.conectar()

# Consulta SQL para obtener datos
consulta_sql = "SELECT * FROM produccion_anp;" 

# Configuración de la página

st.title(" :bar_chart: Dashboard GIMEL H2")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

menu = st.sidebar.radio("Navegación", ["Inicio", "Producción"])
if menu == "Inicio":
    st.subheader("Producción de Energía")
    st.write("Este dashboard está diseñado para tener un entorno que permita visualizar todo el ecosistema de datos de los\
                proyectos en ejecución de GIMEL en tiempo real.")
elif menu == "Producción":
    try:
        df = pd.read_sql(consulta_sql, engine)

        # Convertir la columna 'fecha' a datetime
        df["fecha"] = pd.to_datetime(df["fecha"], format='%Y-%m-%d %H:%M:%S.%f')

        # Obtener el rango de fechas
        start_date = df["fecha"].min()
        end_date = df["fecha"].max()

        st.subheader("Producción de Energía")
        st.write("A continuación puede observar un grafico de línea donnde se representa la producción energetica en el tiempo registrada\
                 por cada uno de los analizadores.")
        st.write("En la parte izquierda podrá filtrar por analizador y también por rango de fechas")

        # Selección de analizador
        analizadores = st.sidebar.multiselect("Elija el analizador de interés", df["analizador"].unique())

        # Selección de rango de fechas
        fecha_inicio = st.sidebar.date_input("Fecha de inicio", start_date)
        fecha_fin = st.sidebar.date_input("Fecha de fin", end_date)

        # Convertir las fechas seleccionadas a datetime
        fecha_inicio = pd.to_datetime(fecha_inicio)
        fecha_fin = pd.to_datetime(fecha_fin)

        # Filtrar el DataFrame según los analizadores y el rango de fechas seleccionados
        if analizadores:
            df_filtrado = df[df["analizador"].isin(analizadores)]
        else:
            df_filtrado = df

        df_filtrado = df_filtrado[(df_filtrado["fecha"] >= fecha_inicio) & (df_filtrado["fecha"] <= fecha_fin)]

        # Mostrar el DataFrame filtrado
        st.dataframe(df_filtrado)

        # Graficar los datos filtrados
        if not df_filtrado.empty:
            st.subheader("Producción energética en el tiempo")
            fig = px.line(
                df_filtrado,
                x="fecha",
                y="producción",
                color="analizador",  
                title="Producción de Energía por Analizador",
                labels={"fecha": "Fecha", "producción": "Producción Energética [W]", "analizador": "Analizador"},
            )
            st.plotly_chart(fig, use_container_width=True)  

            st.subheader("Producción energética total por analizador")
            fig = px.bar(
                df_filtrado,
                x="analizador",
                y="producción",
                color="analizador",  
                title="Producción de Energía por Analizador",
                labels={"fecha": "Fecha", "producción": "Producción Energética [W]", "analizador": "Analizador"},
            )
            st.plotly_chart(fig, use_container_width=True)  
        else:
            st.warning("No hay datos para mostrar con los filtros seleccionados.")


    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")