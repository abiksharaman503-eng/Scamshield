import json
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Incident, Scan
from services.recovery_engine import build_plan
from services.report_generator import generate_report

router = APIRouter(prefix="/api", tags=["incident"])


class IncidentIn(BaseModel):
    scan_id: int | None = None
    country: str = "IN"
    clicked_link: bool = False
    entered_password: bool = False
    entered_otp: bool = False
    entered_card_details: bool = False
    shared_id_documents: bool = False
    downloaded_file: bool = False
    installed_app: bool = False
    gave_remote_access: bool = False
    sent_money: bool = False
    amount: float | None = Field(default=None, ge=0)
    currency: str | None = None
    payment_method: str | None = None       # upi | card | bank_transfer | crypto | gift_card | other
    hours_since: float | None = Field(default=None, ge=0)
    incident_time: str | None = None
    transaction_id: str | None = None
    recipient: str | None = None
    scammer_contact: str | None = None
    notes: str | None = Field(default=None, max_length=3000)


def _scan_dict(db: Session, scan_id: int | None):
    row = db.get(Scan, scan_id) if scan_id else None
    return json.loads(row.result_json) if row else None


@router.post("/incident/assess")
def assess(body: IncidentIn, db: Session = Depends(get_db)):
    plan = build_plan(body.model_dump())
    row = Incident(scan_id=body.scan_id, payload_json=body.model_dump_json(), plan_json=json.dumps(plan))
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"incident_id": row.id, **plan}


@router.get("/incident/{incident_id}/report", response_class=PlainTextResponse)
def report(incident_id: int, db: Session = Depends(get_db)):
    row = db.get(Incident, incident_id)
    if not row:
        raise HTTPException(404, "Incident not found.")
    return generate_report(json.loads(row.payload_json), json.loads(row.plan_json), _scan_dict(db, row.scan_id))


@router.get("/history")
def history(limit: int = 50, db: Session = Depends(get_db)):
    rows = db.query(Scan).order_by(Scan.id.desc()).limit(min(limit, 200)).all()
    return [{"id": r.id, "kind": r.kind, "preview": r.preview, "score": r.score, "level": r.level,
             "created_at": r.created_at.isoformat()} for r in rows]


@router.delete("/history")
def clear_history(db: Session = Depends(get_db)):
    db.query(Scan).delete()
    db.query(Incident).delete()
    db.commit()
    return {"deleted": True}