"""Nexra AI backend. Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import url, message, screenshot, account, incident
from database.database import Base, engine
from database import models  # noqa: F401  (registers tables)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ScamShield AI", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])  # tighten for production

for r in (url.router, message.router, screenshot.router, account.router, incident.router):
    app.include_router(r)


@app.get("/health")
def health():
    return {"status": "ok"}