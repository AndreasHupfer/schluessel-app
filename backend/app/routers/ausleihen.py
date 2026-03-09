from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import Ausleihe, Schluessel, Schliessung, Liegenschaft, Kontakt, SchluesselStatus, AusleiheStatus
from ..schemas import AusleiheCreate, AusleiheUpdate, AusleiheOut, AusleiheWorkflowCreate
from ..pdf_generator import generate_quittung

router = APIRouter(prefix="/ausleihen", tags=["Ausleihen"])


def _load_full(ausleihe_id: int, db: Session) -> Ausleihe:
    obj = (
        db.query(Ausleihe)
        .options(
            joinedload(Ausleihe.schluessel).joinedload(Schluessel.schliessung).joinedload(Schliessung.liegenschaft),
            joinedload(Ausleihe.kontakt),
        )
        .filter(Ausleihe.id == ausleihe_id)
        .first()
    )
    return obj


@router.get("/", response_model=List[AusleiheOut])
def list_ausleihen(schluessel_id: int = None, kontakt_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Ausleihe)
    if schluessel_id:
        q = q.filter(Ausleihe.schluessel_id == schluessel_id)
    if kontakt_id:
        q = q.filter(Ausleihe.kontakt_id == kontakt_id)
    return q.all()


@router.get("/{id}/pdf")
def get_pdf(id: int, db: Session = Depends(get_db)):
    obj = db.query(Ausleihe).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ausleihe nicht gefunden")
    if not obj.quittung_pdf_path:
        raise HTTPException(status_code=404, detail="Kein PDF vorhanden")
    return FileResponse(
        obj.quittung_pdf_path,
        media_type="application/pdf",
        filename=f"quittung_{id}.pdf",
    )


@router.get("/{id}", response_model=AusleiheOut)
def get_ausleihe(id: int, db: Session = Depends(get_db)):
    obj = db.query(Ausleihe).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ausleihe nicht gefunden")
    return obj


@router.post("/checkout", response_model=AusleiheOut, status_code=201)
def checkout(data: AusleiheWorkflowCreate, db: Session = Depends(get_db)):
    """Full checkout workflow: validate key availability, create loan, set key status, generate PDF."""
    schluessel = db.query(Schluessel).get(data.schluessel_id)
    if not schluessel:
        raise HTTPException(status_code=404, detail="Schlüssel nicht gefunden")
    if schluessel.status != SchluesselStatus.verfuegbar:
        raise HTTPException(status_code=400, detail="Schlüssel ist nicht verfügbar")

    kontakt = db.query(Kontakt).get(data.kontakt_id)
    if not kontakt:
        raise HTTPException(status_code=404, detail="Kontakt nicht gefunden")

    ausleihe = Ausleihe(
        schluessel_id=data.schluessel_id,
        kontakt_id=data.kontakt_id,
        ausgabe_datum=date.today(),
        rueckgabe_soll=data.rueckgabe_soll,
        befristet=data.befristet,
        unterschrift_base64=data.unterschrift_base64,
        bemerkung=data.bemerkung,
        status=AusleiheStatus.aktiv,
    )
    db.add(ausleihe)

    schluessel.status = SchluesselStatus.ausgeliehen
    db.flush()  # get ausleihe.id without committing

    # Load relations for PDF
    schliessung = db.query(Schliessung).get(schluessel.schliessung_id)
    liegenschaft = db.query(Liegenschaft).get(schliessung.liegenschaft_id)

    try:
        pdf_path = generate_quittung(ausleihe, schluessel, schliessung, liegenschaft, kontakt)
        ausleihe.quittung_pdf_path = pdf_path
    except Exception as e:
        # PDF failure should not block the checkout
        print(f"PDF generation failed: {e}")

    db.commit()
    db.refresh(ausleihe)
    return ausleihe


@router.post("/{id}/rueckgabe", response_model=AusleiheOut)
def rueckgabe(id: int, db: Session = Depends(get_db)):
    """Mark a loan as returned and set the key back to verfuegbar."""
    obj = db.query(Ausleihe).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Ausleihe nicht gefunden")
    if obj.status != AusleiheStatus.aktiv:
        raise HTTPException(status_code=400, detail="Ausleihe ist nicht aktiv")

    obj.rueckgabe_ist = date.today()
    obj.status = AusleiheStatus.zurueck

    schluessel = db.query(Schluessel).get(obj.schluessel_id)
    if schluessel:
        schluessel.status = SchluesselStatus.verfuegbar

    db.commit()
    db.refresh(obj)
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
