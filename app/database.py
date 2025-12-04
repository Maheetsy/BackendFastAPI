from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
import os

# --- LÓGICA SSL PARA AIVEN ---
connect_args = {}

# Si estamos usando Aiven (lo detectamos por la url), agregamos el certificado
if "aivencloud.com" in settings.database_url:
    # Busca el archivo ca.pem en la misma carpeta donde está este archivo
    ssl_ca_path = os.path.join(os.path.dirname(__file__), "ca.pem")
    
    connect_args = {
        "ssl": {
            "ca": ssl_ca_path
        }
    }

# --- CREAR EL ENGINE CON ARGUMENTOS SSL ---
engine = create_engine(
    settings.database_url, 
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener una sesión de BD en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()