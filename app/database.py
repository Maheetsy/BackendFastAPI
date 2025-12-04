from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
import os

# --- LÓGICA SSL PARA AIVEN ---
connect_args = {}

if "aivencloud.com" in settings.database_url:
    # 1. Primero intentamos buscar en la ruta de secretos de Render
    render_secret_path = "/etc/secrets/ca.pem"
    
    # 2. Si existe el archivo en Render, usamos ese. Si no, usamos el local.
    if os.path.exists(render_secret_path):
        ssl_ca_path = render_secret_path
        print(f"--> Usando certificado de Render: {ssl_ca_path}")
    else:
        # Fallback para tu compu local (busca en la misma carpeta)
        ssl_ca_path = os.path.join(os.path.dirname(__file__), "ca.pem")
        print(f"--> Usando certificado Local: {ssl_ca_path}")
    
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
