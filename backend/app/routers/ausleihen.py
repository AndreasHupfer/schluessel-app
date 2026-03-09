from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Ausleihe
from ..schemas import AusleiheCreate, AusleiheUpdate, AusleiheOut

router = APIRouter(prefix="/ausleihen", tags=["Ausleihen"])


@router.get("/", response_model=List[AusleiheOut])
def list_ausleihen(schluessel_id: int = None, kontakt_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Ausleihe)
    if schluessel_id:
        q = q.filter(Ausleihe.schluessel_id == schluessel_id)
    if kontakt_id:
        q = q.filter(Ausleihe.kontakt_id == kontakt_id)
    return q.all()


@router.get("/{id}", response_model=AusleiheOut)
def get_ausleihe(id: int, db: Session = Depends(get_db)):
    obj = db.query(Ausleihe).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ausleihe nicht gefunden")
    return obj


@router.post("/", response_model=AusleiheOut, status_code=201)
def create_ausleihe(data: AusleiheCreate, db: Session = Depends(get_db)):
    obj = Ausleihe(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=AusleiheOut)
def update_ausleihe(id: int, data: AusleiheUpdate, db: Session = Depends(get_db)):
    obj = db.query(Ausleihe).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ausleihe nicht gefunden")
    for k, v in data.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_ausleihe(id: int, db: Session = Depends(get_db)):
    obj = db.query(Ausleihe).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ausleihe nicht gefunden")
    db.delete(obj)
    db.commit()
