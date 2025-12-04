from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base    # BIEN (sin punto)
from app.models import product, category
from app.routers import product_router, category_router

# --- CORREGIR ESTA LÍNEA ---
# Llama a Base (de database), no a models.Base
Base.metadata.create_all(bind=engine)
# --- FIN DE LÍNEA CORREGIDA ---

app = FastAPI(
    title="API de Productos (Backend 1)",
    description="Servicio en FastAPI/Python para la gestión de productos en SQL."
)

# --- Configuración de CORS ---
origins = [
    "http://localhost",
    "http://localhost:3000", # Asumiendo Flutter web
    # Añade aquí la URL de tu app de Flutter desplegada
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Fin de CORS ---

app.include_router(product_router.router)
app.include_router(category_router.router) # Asegúrate de haber creado este router

@app.get("/")
def read_root():
    return {"Backend": "Backend 1 - FastAPI/Python (Productos)"}