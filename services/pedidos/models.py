from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

from pydantic import BaseModel

# Define la base declarativa
Base = declarative_base()

# TODO: Crea tus modelos de datos aquí.
# Cada clase de modelo representa una tabla en tu base de datos.
# Debes renombrar YourModel por el nombre de la Clase según el servicio
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
    

    # TODO: Agrega más columnas según sea necesario.
    # Por ejemplo:
    # is_active = Column(Boolean, default=True)
    # foreign_key_id = Column(Integer, ForeignKey("otra_tabla.id"))

    def __repr__(self):
        return f"<Order(user_id={self.user_id}, product_id={self.product_id})>"

# TODO: Define los modelos Pydantic para la validación de datos.
# Estos modelos se usarán en los endpoints de FastAPI para validar la entrada y salida.

class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_amount: int
    status: str
    # TODO: Agrega los campos que se necesitan para crear o actualizar un recurso.

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
