from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Liegenschaft
from ..schemas import LiegenschaftCreate, LiegenschaftUpdate, LiegenschaftOut

router = APIRouter(prefix="/liegenschaften", tags=["Liegenschaften"])


@router.get("/", response_model=List[LiegenschaftOut])
def list_liegenschaften(db: Session = Depends(get_db)):
    return db.query(Liegenschaft).all()


@router.get("/{id}", response_model=LiegenschaftOut)
def get_liegenschaft(id: int, db: Session = Depends(get_db)):
    obj = db.query(Liegenschaft).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Liegenschaft nicht gefunden")
    return obj


@router.post("/", response_model=LiegenschaftOut, status_code=201)
def create_liegenschaft(data: LiegenschaftCreate, db: Session = Depends(get_db)):
    obj = Liegenschaft(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/{id}", response_model=LiegenschaftOut)
def update_liegenschaft(id: int, data: LiegenschaftUpdate, db: Session = Depends(get_db)):
    obj = db.query(Liegenschaft).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Liegenschaft nicht gefunden")
    for k, v in data.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
def delete_liegenschaft(id: int, db: Session = Depends(get_db)):
    obj = db.query(Liegenschaft).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Liegenschaft nicht gefunden")
    db.delete(obj)
    db.commit()
