from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

from pydantic import BaseModel

# Define la base declarativa
Base = declarative_base()


class Order(Base):
    """
    Plantilla de modelo de datos para un recurso.
    Ajusta esta clase según los requisitos de tu tema.
    """
    __tablename__ = "orders"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    product_id = Column(Integer, index=True)
    quantity = Column(Integer)
    total_amount = Column(Integer)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Order(user_id={self.user_id}, product_id={self.product_id})>"



class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_amount: int
    status: str
    is_active: bool = True

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    is_active: bool

class OrderUpdate(OrderBase):
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    total_amount: Optional[int] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None
    
    class Config:
        from_attributes = True
