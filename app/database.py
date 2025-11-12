from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Crea el motor de conexión a la BD usando la URL del .env
engine = create_engine(settings.database_url)

# Crea una sesión local (transacciones de la BD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para tus modelos de SQLAlchemy
Base = declarative_base()

# Función para obtener una sesión de BD en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 