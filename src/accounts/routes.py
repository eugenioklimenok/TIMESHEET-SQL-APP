from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.main import db, router
from ..models import AccountCreate, Account
from ..schemas import response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/create")
def create_account(account: AccountCreate, db: Session = Depends(db.get_db)):
    db_account = db.query(Account).filter(Account.email == account.email).first()
    if db_account:
        raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese correo electrónico")
    nuevo_account = Account(email=account.email, password=account.password, nombre=account.nombre, apellido=account.apellido)
    db.add(nuevo_account)
    db.commit()
    db.refresh(nuevo_account)
    return {"message": "Cuenta creada correctamente"}

@router.get("/read")
def read_account(token: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)):
    account = db.query(Account).first()
    return {"message": "Cuenta leída correctamente"}

@router.post("/validate")
def validate_account(form_data: OAuth2PasswordRequestForm = Depends()):
    account = db.query(Account).filter(Account.email == form_data.username).first()
    if not account or not account.password == form_data.password:
        raise HTTPException(status_code=401, detail="Autenticación fallida")
    return {"message": "Cuenta autenticada correctamente"}