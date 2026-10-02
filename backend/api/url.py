import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Scan
from ml.preprocessing import redact
from services.url_analyzer import analyze_url

router = APIRouter(prefix="/api/url", tags=["url"])


class UrlIn(BaseModel):
    url: str = Field(min_length=3, max_length=2048)


def save_scan(db: Session, kind: str, preview: str, result: dict) -> dict:
    row = Scan(kind=kind, preview=redact(preview)[:200], score=result["score"], level=result["level"],
               result_json=json.dumps(result))
    db.add(row)
    db.commit()
    db.refresh(row)
    return {**result, "id": row.id, "kind": kind}


@router.post("/analyze")
def analyze(body: UrlIn, db: Session = Depends(get_db)):
    return save_scan(db, "url", body.url, analyze_url(body.url))