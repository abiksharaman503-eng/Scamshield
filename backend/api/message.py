from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database.database import get_db
from services.nlp_analyzer import analyze_message
from .url import save_scan

router = APIRouter(prefix="/api/message", tags=["message"])


class MessageIn(BaseModel):
    text: str = Field(min_length=3, max_length=10000)


@router.post("/analyze")
def analyze(body: MessageIn, db: Session = Depends(get_db)):
    return save_scan(db, "message", body.text, analyze_message(body.text))