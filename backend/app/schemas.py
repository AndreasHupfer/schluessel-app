from datetime import date
from typing import Optional, List
from pydantic import BaseModel
from .models import SchluesselTyp, SchluesselStatus, KontaktTyp, AusleiheStatus


# --- Liegenschaft ---
class LiegenschaftBase(BaseModel):
    name: str
    adresse: str
    plz: str
    ort: str

class LiegenschaftCreate(LiegenschaftBase):
    pass

class LiegenschaftUpdate(LiegenschaftBase):
    pass

class LiegenschaftOut(LiegenschaftBase):
    id: int
    model_config = {"from_attributes": True}


# --- Schliessung ---
class SchliessungBase(BaseModel):
    liegenschaft_id: int
    bezeichnung: str
    hersteller: Optional[str] = None

class SchliessungCreate(SchliessungBase):
    pass

class SchliessungUpdate(SchliessungBase):
    pass

class SchliessungOut(SchliessungBase):
    id: int
    model_config = {"from_attributes": True}


# --- Schluessel ---
class SchluesselBase(BaseModel):
    schliessung_id: int
    schluessel_nr: str
    laufnummer: Optional[int] = None
    typ: SchluesselTyp = SchluesselTyp.general
    status: SchluesselStatus = SchluesselStatus.verfuegbar

class SchluesselCreate(SchluesselBase):
    pass

class SchluesselUpdate(SchluesselBase):
    pass

class SchluesselOut(SchluesselBase):
    id: int
    model_config = {"from_attributes": True}


# --- Kontakt ---
class KontaktBase(BaseModel):
    typ: KontaktTyp
    firma: Optional[str] = None
    vorname: Optional[str] = None
    nachname: str
    email: Optional[str] = None
    telefon: Optional[str] = None

class KontaktCreate(KontaktBase):
    pass

class KontaktUpdate(KontaktBase):
    pass

class KontaktOut(KontaktBase):
    id: int
    model_config = {"from_attributes": True}


# --- Ausleihe ---
class AusleiheBase(BaseModel):
    schluessel_id: int
    kontakt_id: int
    ausgabe_datum: date
    rueckgabe_soll: Optional[date] = None
    rueckgabe_ist: Optional[date] = None
    befristet: bool = False
    unterschrift_base64: Optional[str] = None
    quittung_pdf_path: Optional[str] = None
    status: AusleiheStatus = AusleiheStatus.aktiv

class AusleiheCreate(AusleiheBase):
    pass

class AusleiheUpdate(AusleiheBase):
    pass

class AusleiheOut(AusleiheBase):
    id: int
    model_config = {"from_attributes": True}
