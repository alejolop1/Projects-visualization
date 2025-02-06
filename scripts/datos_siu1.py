import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Lista de valores posibles para 'analizador'
analizadores = ['Anp01', 'Anp02', 'Anp03', 'Anp04', 'Anp05']

# Rango de fechas (un año, día a día)
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
dates = pd.date_range(start_date, end_date, freq='D')

# Generar los datos de producción de energía aleatorios (valores entre 100 y 1000)
produccion = np.random.randint(100, 1001, size=len(dates))

# Crear la tabla
data = {
    'fecha': dates,
    'analizador': np.random.choice(analizadores, size=len(dates)),
    'producción': produccion
}

# Crear el DataFrame de pandas
df = pd.DataFrame(data)

# Mostrar la tabla
print(df)


# Configura la conexión a MySQL
usuario = 'root'
contraseña = 'hnai7lc2004'
host = 'localhost'  # o la dirección del servidor MySQL
base_de_datos = 'aprendiendo_sql'

# Crea la cadena de conexión
cadena_conexion = f'mysql+mysqlconnector://{usuario}:{contraseña}@{host}/{base_de_datos}'

# Crea el motor de SQLAlchemy
engine = create_engine(cadena_conexion)

nombre_tabla = 'produccion_anp'  # Nombre de la tabla que se creará en MySQL

# Subir el DataFrame a MySQL
df.to_sql(
    name=nombre_tabla,  # Nombre de la tabla
    con=engine,         # Conexión a la base de datos
    if_exists='replace',  # Reemplaza la tabla si ya existe
    index=False          # No incluir el índice del DataFrame en la tabla
)

#print(f"Tabla '{nombre_tabla}' creada y datos subidos correctamente.")


