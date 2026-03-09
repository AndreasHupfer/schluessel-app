from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Kontakt
from ..schemas import KontaktCreate, KontaktUpdate, KontaktOut

router = APIRouter(prefix="/kontakte", tags=["Kontakte"])


@router.get("/", response_model=List[KontaktOut])
def list_kontakte(db: Session = Depends(get_db)):
    return db.query(Kontakt).all()


@router.get("/{id}", response_model=KontaktOut)
def get_kontakt(id: int, db: Session = Depends(get_db)):
    obj = db.query(Kontakt).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Kontakt nicht gefunden")
    return obj


@router.post("/", response_model=KontaktOut, status_code=201)
def create_kontakt(data: KontaktCreate, db: Session = Depends(get_db)):
    obj = Kontakt(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=KontaktOut)
def update_kontakt(id: int, data: KontaktUpdate, db: Session = Depends(get_db)):
    obj = db.query(Kontakt).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Kontakt nicht gefunden")
    for k, v in data.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_kontakt(id: int, db: Session = Depends(get_db)):
    obj = db.query(Kontakt).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Kontakt nicht gefunden")
    db.delete(obj)
    db.commit()
