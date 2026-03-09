from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Schliessung
from ..schemas import SchliessungCreate, SchliessungUpdate, SchliessungOut

router = APIRouter(prefix="/schliessungen", tags=["Schliessungen"])


@router.get("/", response_model=List[SchliessungOut])
def list_schliessungen(liegenschaft_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Schliessung)
    if liegenschaft_id:
        q = q.filter(Schliessung.liegenschaft_id == liegenschaft_id)
    return q.all()


@router.get("/{id}", response_model=SchliessungOut)
def get_schliessung(id: int, db: Session = Depends(get_db)):
    obj = db.query(Schliessung).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Schliessung nicht gefunden")
    return obj


@router.post("/", response_model=SchliessungOut, status_code=201)
def create_schliessung(data: SchliessungCreate, db: Session = Depends(get_db)):
    obj = Schliessung(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=SchliessungOut)
def update_schliessung(id: int, data: SchliessungUpdate, db: Session = Depends(get_db)):
    obj = db.query(Schliessung).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Schliessung nicht gefunden")
    for k, v in data.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_schliessung(id: int, db: Session = Depends(get_db)):
    obj = db.query(Schliessung).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Schliessung nicht gefunden")
    db.delete(obj)
    db.commit()
