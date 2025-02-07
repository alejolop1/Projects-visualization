import streamlit as st
from connection_VE import MySQLConnection




st.set_page_config(page_title="Dashboard GIMEL", page_icon=":bar_chart:", layout="wide")

# Crear la conexión
conexion = MySQLConnection()
engine = conexion.conectar()

st.title(" :bar_chart: Dashboard GIMEL H2")
#st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

st.write("Bienvenido al Dashboard de GIMEL")

st.title("Inicio")

st.write(
    "Este dashboard está diseñado para visualizar el ecosistema de datos "
    "de los proyectos en ejecución de GIMEL en tiempo real."
)