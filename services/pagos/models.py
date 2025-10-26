from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

from pydantic import BaseModel


# Define la base declarativa
Base = declarative_base()


class Payment(Base):
    """
    Plantilla de modelo de datos para un recurso.
    Ajusta esta clase según los requisitos de tu tema.
    """
    __tablename__ = "payments"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # ID del usuario (cliente o vendedor)
    order_id = Column(Integer, index=True)  # ID del pedido relacionado
    amount = Column(Integer)  # Monto en centavos para precisión
    currency = Column(String, default="COP")
    status = Column(String, default="pending")  # Ej. pending, completed, failed
    payment_method = Column(String)  # Ej. credit_card, paypal
    created_at = Column(DateTime, default=datetime.utcnow)

    #agrego columna adicional de pagos
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount})>"

class PaymentBase(BaseModel):
    user_id: int
    order_id: int
    amount: int
    currency: str = "COP" 
    payment_method: str
    is_active: bool = True
    updated_at: Optional[datetime] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class PaymentUpdate(PaymentBase):
    user_id: Optional[int] = None
    order_id: Optional[int] = None
    amount: Optional[int] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    is_active: Optional[bool] = None
    
    class Config:
        from_attributes = True # Compatibilidad con Pydantic V2
