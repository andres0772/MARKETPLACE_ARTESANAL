from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

from pydantic import BaseModel
from typing import Optional

# Define la base declarativa
Base = declarative_base()

# TODO: Crea tus modelos de datos aquí.
# Cada clase de modelo representa una tabla en tu base de datos.
# Debes renombrar YourModel por el nombre de la Clase según el servicio
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

    # TODO: Agrega más columnas según sea necesario.
    # Por ejemplo:
    # is_active = Column(Boolean, default=True)
    # foreign_key_id = Column(Integer, ForeignKey("otra_tabla.id"))

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount})>"

# TODO: Define los modelos Pydantic para la validación de datos.
# Estos modelos se usarán en los endpoints de FastAPI para validar la entrada y salida.

class PaymentBase(BaseModel):
    user_id: int
    order_id: int
    amount: int
    currency: str = "COP" 
    payment_method: str
    # TODO: Agrega los campos que se necesitan para crear o actualizar un recurso.

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int
    status: str
    created_at: datetime
    
    class Config:
        orm_mode = True # Habilita la compatibilidad con ORM
