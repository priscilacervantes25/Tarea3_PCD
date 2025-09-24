import os
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from sqlalchemy.orm import Session
from dotenv import load_dotenv

import models
from database import engine, SessionLocal

# ----- Cargar variables de entorno (.env) -----
load_dotenv()
API_KEY = os.getenv("API_KEY")

# ----- Iniciar app -----
app = FastAPI(title="Users API", version="1.0.0")

# ----- Crear tablas -----
models.Base.metadata.create_all(bind=engine)

# ----- Dependencia DB -----
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# ----- Seguridad por header -----
api_key_header = APIKeyHeader(name="X-API-Key", description="API key por header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

# ----- Esquema Pydantic -----
class User(BaseModel):
    user_name: str = Field(min_length=1)
    user_id: int
    user_email: str = Field(min_length=1, max_length=100)
    age: Optional[int] = None
    recommendations: List[str] = []
    ZIP: Optional[str] = None

# ----- Endpoints -----
@app.get("/")
def root():
    return {"message": "Users API up. See /docs"}

# 1) Crear usuario
@app.post("/api/v1/users/", tags=["users"])
def create_user(user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    # Verificar si ya existe ese email
    existing_user = db.query(models.Users).filter(models.Users.user_email == user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail=f"Email {user.user_email} already exists")

    user_model = models.Users(
        user_name=user.user_name,
        user_id=user.user_id,
        user_email=user.user_email,
        age=user.age,
        recommendations=",".join(user.recommendations),  # guardamos como string separado por comas
        ZIP=user.ZIP
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

# 2) Actualizar usuario
@app.put("/api/v1/users/{user_id}", tags=["users"])
def update_user(user_id: int, user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")

    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = ",".join(user.recommendations)
    user_model.ZIP = user.ZIP

    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

# 3) Obtener usuario
@app.get("/api/v1/users/{user_id}", tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")
    return user_model

# 4) Eliminar usuario
@app.delete("/api/v1/users/{user_id}", tags=["users"])
def delete_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id} : Does not exist")

    db.query(models.Users).filter(models.Users.user_id == user_id).delete()
    db.commit()
    return {"deleted_id": user_id}

