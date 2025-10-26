from fastapi import FastAPI, APIRouter
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Producto, ProductoCreate, ProductoResponse

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/productos_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

router = APIRouter()

# TODO: Define un endpoint raíz o de salud para verificar que el servicio está funcionando
@app.get("/")
def read_root():
    return {"message": "Servicio de [nombre_del_servicio] en funcionamiento."}

@app.get("/health")
def health_check():
    """Endpoint de salud para verificar el estado del servicio."""
    return {"status": "ok"}

# Endpoints en el router para productos
@router.get("/productos/", response_model=list[ProductoResponse])
async def get_productos():
    db = SessionLocal()
    productos = db.query(Producto).all()
    db.close()
    return productos


@router.post("/productos/", response_model=ProductoResponse)
async def create_producto(producto: ProductoCreate):
    db = SessionLocal()
    new_producto = Producto(**producto.dict())
    db.add(new_producto)
    db.commit()
    db.refresh(new_producto)
    db.close()
    return new_producto


app.include_router(router, prefix="/api/v1")
