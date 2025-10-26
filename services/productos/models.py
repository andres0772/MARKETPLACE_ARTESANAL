from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

# Define la base declarativa
Base = declarative_base()

# TODO: Crea tus modelos de datos aquí.
# Cada clase de modelo representa una tabla en tu base de datos.
# Debes renombrar YourModel por el nombre de la Clase según el servicio
class Producto(Base):
    """
    Plantilla de modelo de datos para un recurso.
    Ajusta esta clase según los requisitos de tu tema.
    """
    __tablename__ = "productos"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio = Column(Float)
    categoria = Column(String)
    image = Column(String)
    is_active = Column(Boolean, default=True)
    


    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}')>"


class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    image: Optional[str] = None
    is_active: bool = True

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    image: Optional[str] = None
    is_active: bool = True
    
    class Config:
        from_attributes = True
