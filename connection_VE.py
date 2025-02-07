import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

        # Crear el motor de SQLAlchemy con un pool de conexiones
        self.engine = self.conectar()

        # Crear una fábrica de sesiones
        self.Session = sessionmaker(bind=self.engine)

    def conectar(self):
        # Construir la cadena de conexión
        cadena_conexion = (
            f'mysql+mysqlconnector://{self.credenciales["user"]}:{self.credenciales["password"]}'
            f'@{self.credenciales["host"]}:{self.credenciales["port"]}/{self.credenciales["database"]}'
        )
        
        # Crear el motor de SQLAlchemy con configuración del pool
        engine = create_engine(
            cadena_conexion,
            pool_size=5,          # Número máximo de conexiones en el pool
            max_overflow=10,      # Número máximo de conexiones adicionales si el pool está lleno
            pool_timeout=30,      # Tiempo máximo de espera para obtener una conexión (en segundos)
            pool_recycle=3600     # Reciclar conexiones después de 1 hora (evita problemas con timeouts)
        )
        return engine

    def obtener_sesion(self):
        # Obtener una nueva sesión desde el pool
        return self.Session()

    def cerrar_sesion(self, session):
        # Cerrar la sesión
        if session:
            session.close()

    def cerrar_conexion(self):
        # Cerrar todas las conexiones del pool
        if self.engine:
            self.engine.dispose()