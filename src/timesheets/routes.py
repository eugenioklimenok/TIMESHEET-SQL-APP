from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.main import db, router
from ..models import TimesheetCreate, Timesheet
from ..schemas import response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/timesheets", tags=["timesheets"])

@router.post("/create")
def create_timesheet(timesheet: TimesheetCreate, db: Session = Depends(db.get_db)):
    db_timesheet = db.query(Timesheet).filter(Timesheet.project_id == timesheet.project_id).first()
    if db_timesheet:
        raise HTTPException(status_code=400, detail="Ya existe una vez de trabajo para ese proyecto")
    nuevo_timesheet = Timesheet(project_id=timesheet.project_id, start_date=timesheet.start_date, end_date=timesheet.end_date, hours_worked=timesheet.hours_worked)
    db.add(nuevo_timesheet)
    db.commit()
    db.refresh(nuevo_timesheet)
    return {"message": "Tiempo de trabajo creado correctamente"}

@router.get("/read")
def read_timesheet(token: str = Depends(oauth2_scheme), db: Session = Depends(db.get_db)):
    timesheet = db.query(Timesheet).first()
    return {"message": "Tiempo de trabajo leído correctamente"}

@router.post("/validate")
def validate_timesheet(form_data: OAuth2PasswordRequestForm = Depends()):
    timesheet = db.query(Timesheet).filter(Timesheet.project_id == form_data.username).first()
    if not timesheet or not timesheet.start_date == form_data.password:
        raise HTTPException(status_code=401, detail="Autenticación fallida")
    return {"message": "Tiempo de trabajo autenticado correctamente"}