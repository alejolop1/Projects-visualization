import json
from sqlalchemy import create_engine
import os

class MySQLConnection:
    def __init__(self, credenciales_path=None):
        # Obtener la ruta del directorio base del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  
        if credenciales_path is None:
            credenciales_path = os.path.join(base_dir, "config", "credenciales.json")  # Ruta correcta
        
        # Cargar credenciales desde el archivo JSON
        try:
            with open(credenciales_path, "r") as file:
                self.credenciales = json.load(file)
        except Exception as e:
            raise Exception(f"Error al cargar credenciales: {e}")

    def conectar(self):
        from sqlalchemy import create_engine
        
        usuario = self.credenciales["user"]
        contraseña = self.credenciales["password"]
        host = self.credenciales["host"]
        base_de_datos = self.credenciales["database"]
        puerto = self.credenciales.get("port", 3306)  

        # Cadena de conexión SQLAlchemy
        cadena_conexion = f'mysql+mysqlconnector://{usuario}:{contraseña}@{host}:{puerto}/{base_de_datos}'
        
        # Crear el motor de SQLAlchemy
        engine = create_engine(cadena_conexion)
        return engine
    
    def cerrar_conexion(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None