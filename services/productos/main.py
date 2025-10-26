from fastapi import FastAPI, APIRouter, Depends, HTTPException
import os

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Producto, ProductoCreate, ProductoResponse

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/productos_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
async def get_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()


@router.post("/productos/", response_model=ProductoResponse)
async def create_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    new_producto = Producto(**producto.dict())
    db.add(new_producto)
    db.commit()
    db.refresh(new_producto)
    return new_producto

@router.put("/productos/{id}", response_model=ProductoResponse)
async def update_producto(id: int, producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/productos/{id}")
async def delete_producto(id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return {"message": "Producto eliminado"}
    



app.include_router(router, prefix="/api/v1")
