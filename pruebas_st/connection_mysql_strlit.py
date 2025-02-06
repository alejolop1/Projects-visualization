import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px

# Función para obtener datos de la base de datos
def get_data_from_db():
    connection = mysql.connector.connect(
        host="localhost",      # Cambia por la dirección de tu servidor MySQL
        user="root",           # Usuario de la base de datos
        password="hnai7lc2004", # Contraseña del usuario
        database="database_fincas_local"  # Nombre de la base de datos
    )
    query = "SELECT * FROM datos_meteorologicos"
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# Configuración del dashboard
st.set_page_config(
    page_title="Dashboard Fincas",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Dashboard en Tiempo Real - Fincas")
st.markdown("### Visualización y análisis de datos meteorológicos")

# Menú en la barra lateral
menu = st.sidebar.radio("Navegación", ["Inicio", "Datos", "Gráficos", "Configuración"])

# Contenido de cada sección
if menu == "Inicio":
    st.subheader("Bienvenido al Dashboard")
    st.write("Utiliza las opciones en la barra lateral para navegar por el dashboard.")
    st.image("https://via.placeholder.com/800x300.png?text=Dashboard+Fincas", use_column_width=True)

elif menu == "Datos":
    st.subheader("Datos en tiempo real")
    if st.button("Actualizar Datos"):
        data = get_data_from_db()
        st.dataframe(data)
    else:
        st.write("Haz clic en 'Actualizar Datos' para refrescar los datos.")

elif menu == "Gráficos":
    st.subheader("Análisis Gráfico")
    data = get_data_from_db()

    # Selección de columnas
    columns = list(data.columns)
    x_axis = st.selectbox("Selecciona el eje X", columns)
    y_axis = st.selectbox("Selecciona el eje Y", columns)

    # Gráfico interactivo con Plotly
    if x_axis and y_axis:
        fig = px.scatter(data, x=x_axis, y=y_axis, title=f"Gráfico {x_axis} vs {y_axis}")
        st.plotly_chart(fig, use_container_width=True)

elif menu == "Configuración":
    st.subheader("Configuraciones")
    st.write("Aquí puedes configurar opciones del dashboard.")

# Pie de página
st.markdown("---")
st.markdown("**Dashboard desarrollado con Streamlit**")
