from fastapi import FastAPI, APIRouter
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Order, OrderCreate, OrderRead, OrderUpdate, Base
from fastapi import Depends
from typing import List
from fastapi import HTTPException

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5433/pedidos_db")
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


@app.get("/")
def read_root():
    return {"message": "Servicio de pedidos en funcionamiento."}

@app.get("/health")
def health_check():
    """Endpoint de salud para verificar el estado del servicio."""
    return {"status": "ok"}

@router.get("/pedidos/", response_model=List[OrderRead])
async def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@router.post("/pedidos/", response_model=OrderRead)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.put("/pedidos/{id}", response_model=OrderRead)
async def update_order(id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/pedidos/{id}")
async def delete_order(id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    db.delete(db_order)
    db.commit()
    return {"message": "Pedido eliminado correctamente"}

app.include_router(router, prefix="/api/v1")