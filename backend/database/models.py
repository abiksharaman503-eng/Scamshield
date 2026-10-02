from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from .database import Base


def _now():
    return datetime.now(timezone.utc)


class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String(20), index=True)          # url | message | screenshot | account
    preview = Column(String(200))                   # REDACTED short preview only
    score = Column(Float)
    level = Column(String(12))
    result_json = Column(Text)
    created_at = Column(DateTime(timezone=True), default=_now)


class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, nullable=True)
    payload_json = Column(Text)
    plan_json = Column(Text)
    created_at = Column(DateTime(timezone=True), default=_now)