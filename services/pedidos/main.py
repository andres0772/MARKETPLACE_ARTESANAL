from fastapi import FastAPI, APIRouter
import os

from database import get_db, engine
from models import Order, OrderCreate, OrderRead, Base
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import List

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5433/pedidos_db")

Base.metadata.create_all(bind=engine)

app = FastAPI()


router = APIRouter()


@app.get("/")
def read_root():
    return {"message": "Servicio de pedidos en funcionamiento."}

@app.get("/health")
def health_check():
    """Endpoint de salud para verificar el estado del servicio."""
    return {"status": "ok"}

@router.post("/orders", response_model=OrderRead)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders", response_model=List[OrderRead])
async def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


app.include_router(router, prefix="/api/v1")