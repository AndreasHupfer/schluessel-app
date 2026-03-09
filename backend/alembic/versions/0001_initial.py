"""initial

Revision ID: 0001
Revises:
Create Date: 2026-01-01 00:00:00.000000

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "liegenschaften",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("adresse", sa.String(), nullable=False),
        sa.Column("plz", sa.String(length=10), nullable=False),
        sa.Column("ort", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_liegenschaften_id"), "liegenschaften", ["id"], unique=False)

    op.create_table(
        "schliessungen",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("liegenschaft_id", sa.Integer(), nullable=False),
        sa.Column("bezeichnung", sa.String(), nullable=False),
        sa.Column("hersteller", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["liegenschaft_id"], ["liegenschaften.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_schliessungen_id"), "schliessungen", ["id"], unique=False)

    op.create_table(
        "schluessel",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("schliessung_id", sa.Integer(), nullable=False),
        sa.Column("schluessel_nr", sa.String(), nullable=False),
        sa.Column("laufnummer", sa.Integer(), nullable=True),
        sa.Column("typ", sa.Enum("general", "hauswart", "lift", "wohnung", "sonstige", name="schluesseltyp"), nullable=False),
        sa.Column("status", sa.Enum("verfuegbar", "ausgeliehen", "verloren", name="schluesselstatus"), nullable=False),
        sa.ForeignKeyConstraint(["schliessung_id"], ["schliessungen.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_schluessel_id"), "schluessel", ["id"], unique=False)

    op.create_table(
        "kontakte",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("typ", sa.Enum("handwerker", "mieter", name="kontakttyp"), nullable=False),
        sa.Column("firma", sa.String(), nullable=True),
        sa.Column("vorname", sa.String(), nullable=True),
        sa.Column("nachname", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("telefon", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_kontakte_id"), "kontakte", ["id"], unique=False)

    op.create_table(
        "ausleihen",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("schluessel_id", sa.Integer(), nullable=False),
        sa.Column("kontakt_id", sa.Integer(), nullable=False),
        sa.Column("ausgabe_datum", sa.Date(), nullable=False),
        sa.Column("rueckgabe_soll", sa.Date(), nullable=True),
        sa.Column("rueckgabe_ist", sa.Date(), nullable=True),
        sa.Column("befristet", sa.Boolean(), nullable=False),
        sa.Column("unterschrift_base64", sa.Text(), nullable=True),
        sa.Column("quittung_pdf_path", sa.String(), nullable=True),
        sa.Column("status", sa.Enum("aktiv", "zurueck", "ueberfaellig", name="ausleihestatus"), nullable=False),
        sa.ForeignKeyConstraint(["schluessel_id"], ["schluessel.id"]),
        sa.ForeignKeyConstraint(["kontakt_id"], ["kontakte.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ausleihen_id"), "ausleihen", ["id"], unique=False)


def downgrade() -> None:
    op.drop_table("ausleihen")
    op.drop_table("kontakte")
    op.drop_table("schluessel")
    op.drop_table("schliessungen")
    op.drop_table("liegenschaften")
    op.execute("DROP TYPE IF EXISTS ausleihestatus")
    op.execute("DROP TYPE IF EXISTS kontakttyp")
    op.execute("DROP TYPE IF EXISTS schluesselstatus")
    op.execute("DROP TYPE IF EXISTS schluesseltyp")
