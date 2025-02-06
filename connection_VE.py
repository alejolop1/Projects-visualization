import os
from sqlalchemy import create_engine
import json

class MySQLConnection:
    def __init__(self):
        # Obtener credenciales desde variables de entorno
        self.credenciales = {
            "user": os.getenv("DB_USER"),          # Nombre de usuario de la base de datos
            "password": os.getenv("DB_PASSWORD"),  # Contraseña de la base de datos
            "host": os.getenv("DB_HOST"),          # Host de la base de datos
            "database": os.getenv("DB_NAME"),      # Nombre de la base de datos
            "port": os.getenv("DB_PORT", 3306)     # Puerto (opcional, por defecto 3306)
        }

        # Verificar que todas las credenciales estén presentes
        for key, value in self.credenciales.items():
            if value is None:
                raise Exception(f"Falta la variable de entorno: {key}")

    def conectar(self):
        # Construir la cadena de conexión
        cadena_conexion = (
            f'mysql+mysqlconnector://{self.credenciales["user"]}:{self.credenciales["password"]}'
            f'@{self.credenciales["host"]}:{self.credenciales["port"]}/{self.credenciales["database"]}'
        )
        
        # Crear el motor de SQLAlchemy
        engine = create_engine(cadena_conexion)
        return engine
    
    def cerrar_conexion(self, engine):
        if engine:
            engine.dispose()