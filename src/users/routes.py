from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.main import db, router
from ..models import UserCreate, User
from ..schemas import response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create")
def create_user(user: UserCreate, db: Session = Depends(db.get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo electrónico")
    nuevo_user = User(email=user.email, password=user.password, nombre=user.nombre, apellido=user.apellido)
    db.add(nuevo_user)
    db.commit()
    db.refresh(nuevo_user)
    return {"message": "Usuario creado correctamente"}

@router.get("/read")
def read_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)):
    user = db.query(User).first()
    return {"message": "Usuario leído correctamente"}

@router.post("/validate")
def validate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.password == form_data.password:
        raise HTTPException(status_code=401, detail="Autenticación fallida")
    return {"message": "Usuario autenticado correctamente"}