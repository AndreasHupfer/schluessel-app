from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Schluessel
from ..schemas import SchluesselCreate, SchluesselUpdate, SchluesselOut

router = APIRouter(prefix="/schluessel", tags=["Schluessel"])


@router.get("/", response_model=List[SchluesselOut])
def list_schluessel(schliessung_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Schluessel)
    if schliessung_id:
        q = q.filter(Schluessel.schliessung_id == schliessung_id)
    return q.all()


@router.get("/{id}", response_model=SchluesselOut)
def get_schluessel(id: int, db: Session = Depends(get_db)):
    obj = db.query(Schluessel).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Schluessel nicht gefunden")
    return obj


@router.post("/", response_model=SchluesselOut, status_code=201)
def create_schluessel(data: SchluesselCreate, db: Session = Depends(get_db)):
    obj = Schluessel(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=SchluesselOut)
def update_schluessel(id: int, data: SchluesselUpdate, db: Session = Depends(get_db)):
    obj = db.query(Schluessel).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Schluessel nicht gefunden")
    for k, v in data.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_schluessel(id: int, db: Session = Depends(get_db)):
    obj = db.query(Schluessel).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Schluessel nicht gefunden")
    db.delete(obj)
    db.commit()
