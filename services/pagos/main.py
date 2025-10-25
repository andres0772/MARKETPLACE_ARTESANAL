from fastapi import FastAPI, APIRouter
import os

from .database import get_db #para la sesion de BD
from .models import Payment, PaymentCreate, PaymentRead  # Modelos personalizados
from sqlalchemy.orm import Session
from fastapi import Depends

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/pagos_db")

app = FastAPI()

router = APIRouter()

@app.get("/")
def read_root():
    return {"message": "Servicio de pagos en funcionamiento."}

@app.get("/health")
def health_check():
    """Endpoint de salud para verificar el estado del servicio."""
    return {"status": "ok"}

@router.post("/payments", response_model=PaymentRead)
async def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment
    


app.include_router(router, prefix="/api/v1")
