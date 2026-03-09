from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import liegenschaften, schliessungen, schluessel, kontakte, ausleihen

app = FastAPI(title="Schluessel-Manager API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(liegenschaften.router, prefix="/api")
app.include_router(schliessungen.router, prefix="/api")
app.include_router(schluessel.router, prefix="/api")
app.include_router(kontakte.router, prefix="/api")
app.include_router(ausleihen.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Schluessel-Manager API"}
