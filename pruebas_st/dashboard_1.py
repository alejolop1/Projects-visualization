import streamlit as st
import plotly.express as px
import mysql.connector
import os
import pandas as pd


#CONEXION BASE DE DATOS
def get_data_from_db():
    connection = mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="hnai7lc2004", 
        database="database_fincas_local"  
    )
    query = "SELECT * FROM datos_meteorologicos"
    data = pd.read_sql(query, connection)
    connection.close()
    return data


#DASHBOARD CON STREAMLIT
st.set_page_config(page_title="Dashboard GIMEL", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Dashboard GIMEL H2")
#st.markdown('<style>div.block-container{padding-top:1rem;}</style', unsafe_allow_html=True)
menu = st.sidebar.radio("Navegación", ["Resumen", "Datos", "Gráficos"])

data = get_data_from_db()
c1, c2 = st.columns((2))

data["fecha_medicion"] = pd.to_datetime(data["fecha_medicion"], format='%Y-%m-%d %H:%M:%S.%f')

start = pd.to_datetime(data["fecha_medicion"]).min()
finish = pd.to_datetime(data["fecha_medicion"]).max()


if menu == "Resumen":
    st.subheader("Resumen")
    st.write("Este dashboard está diseñado para tener un entorno que permita visualizar todo el ecosistema de datos de los\
             proyectos en ejecución de GIMEL en tiempo real.")
    st.write("En la sección lateral de la izquierda, encontrará un menú que lo llevará o bien sea a los datos de MySQL en tiempo\
             , o a la sección para visualizar la base de datos con diferentes tipos de gráficos")
    #st.image("https://via.placeholder.com/800x300.png?text=Dashboard+Fincas", use_column_width=True)


elif menu == "Datos":
    st.subheader("Datos en tiempo real de base de datos del proyecto SIATA")
    #with c1:
    #    date1 = pd.to_datetime(st.date_input("Fecha de inicio", start))
    #with c2:
    #    date2 = pd.to_datetime(st.date_input("Fecha de finalización", finish))
    #data = data[(data["fecha_medicion"] >= date1) & (data["fecha_medicion"] <= date2)].copy()
    if st.button("Actualizar Datos"):
        st.dataframe(data)
    else:
        st.write("Haz clic en 'Actualizar Datos' para refrescar los datos. Esto permitirá mostrar \
                 cualquier tipo de modificación realizada en la base de datos.")
        

elif menu == "Gráficos":
    st.subheader("Análisis Gráfico")
    estacion = st.sidebar.multiselect("Elija la estación de interes", data["nombre_estacion"].unique())
    with c1:
        columns = list(data.columns)
        x_axis = st.selectbox("Selecciona el eje X", columns)
        y_axis = st.selectbox("Selecciona el eje Y", columns)
        
        if x_axis and y_axis:
            fig = px.scatter(data, x=x_axis, y=y_axis, title=f"Gráfico {x_axis} vs {y_axis}")
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        #columns = list(data.columns)
        #x_axis = st.selectbox("Selecciona el eje X", columns)
        #y_axis = st.selectbox("Selecciona el eje Y", columns)

        
        #if x_axis and y_axis:
        fig = px.bar(data, x=x_axis, y=y_axis, title=f"Gráfico {x_axis} vs {y_axis}")
        st.plotly_chart(fig, use_container_width=True)