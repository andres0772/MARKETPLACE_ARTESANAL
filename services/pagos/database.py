from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

#Configura la URL de la BD desde variables de entorno (como en docker-compose.yml)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/pagos_db")

#Crea el motor de la base de datos
engine = create_engine(DATABASE_URL)

#crea una sesion local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#dependencias para obtener la sesion de la base de datos en Fastapi

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()