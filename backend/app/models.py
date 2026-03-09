import enum
from datetime import date
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from .database import Base


class SchluesselTyp(str, enum.Enum):
    general = "general"
    hauswart = "hauswart"
    lift = "lift"
    wohnung = "wohnung"
    sonstige = "sonstige"


class SchluesselStatus(str, enum.Enum):
    verfuegbar = "verfuegbar"
    ausgeliehen = "ausgeliehen"
    verloren = "verloren"


class KontaktTyp(str, enum.Enum):
    handwerker = "handwerker"
    mieter = "mieter"


class AusleiheStatus(str, enum.Enum):
    aktiv = "aktiv"
    zurueck = "zurueck"
    ueberfaellig = "ueberfaellig"


class Liegenschaft(Base):
    __tablename__ = "liegenschaften"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    adresse = Column(String, nullable=False)
    plz = Column(String(10), nullable=False)
    ort = Column(String, nullable=False)

    schliessungen = relationship("Schliessung", back_populates="liegenschaft", cascade="all, delete-orphan")


class Schliessung(Base):
    __tablename__ = "schliessungen"

    id = Column(Integer, primary_key=True, index=True)
    liegenschaft_id = Column(Integer, ForeignKey("liegenschaften.id"), nullable=False)
    bezeichnung = Column(String, nullable=False)
    hersteller = Column(String, nullable=True)

    liegenschaft = relationship("Liegenschaft", back_populates="schliessungen")
    schluessel = relationship("Schluessel", back_populates="schliessung", cascade="all, delete-orphan")


class Schluessel(Base):
    __tablename__ = "schluessel"

    id = Column(Integer, primary_key=True, index=True)
    schliessung_id = Column(Integer, ForeignKey("schliessungen.id"), nullable=False)
    schluessel_nr = Column(String, nullable=False)
    laufnummer = Column(Integer, nullable=True)
    typ = Column(Enum(SchluesselTyp), nullable=False, default=SchluesselTyp.general)
    status = Column(Enum(SchluesselStatus), nullable=False, default=SchluesselStatus.verfuegbar)

    schliessung = relationship("Schliessung", back_populates="schluessel")
    ausleihen = relationship("Ausleihe", back_populates="schluessel")


class Kontakt(Base):
    __tablename__ = "kontakte"

    id = Column(Integer, primary_key=True, index=True)
    typ = Column(Enum(KontaktTyp), nullable=False)
    firma = Column(String, nullable=True)
    vorname = Column(String, nullable=True)
    nachname = Column(String, nullable=False)
    email = Column(String, nullable=True)
    telefon = Column(String, nullable=True)

    ausleihen = relationship("Ausleihe", back_populates="kontakt")


class Ausleihe(Base):
    __tablename__ = "ausleihen"

    id = Column(Integer, primary_key=True, index=True)
    schluessel_id = Column(Integer, ForeignKey("schluessel.id"), nullable=False)
    kontakt_id = Column(Integer, ForeignKey("kontakte.id"), nullable=False)
    ausgabe_datum = Column(Date, nullable=False, default=date.today)
    rueckgabe_soll = Column(Date, nullable=True)
    rueckgabe_ist = Column(Date, nullable=True)
    befristet = Column(Boolean, nullable=False, default=False)
    unterschrift_base64 = Column(Text, nullable=True)
    bemerkung = Column(Text, nullable=True)
    quittung_pdf_path = Column(String, nullable=True)
    status = Column(Enum(AusleiheStatus), nullable=False, default=AusleiheStatus.aktiv)

    schluessel = relationship("Schluessel", back_populates="ausleihen")
    kontakt = relationship("Kontakt", back_populates="ausleihen")
