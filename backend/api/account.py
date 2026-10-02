from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.database import get_db
from services.account_analyzer import analyze_account
from .url import save_scan

router = APIRouter(prefix="/api/account", tags=["account"])


class AccountIn(BaseModel):
    platform: str | None = None
    username: str | None = None
    display_name: str | None = None
    bio: str | None = None
    followers: int | None = None
    following: int | None = None
    post_count: int | None = None
    account_age_days: int | None = None
    has_profile_photo: bool | None = None
    asked_for_money: bool = False
    moved_to_private_chat: bool = False
    claims_investment_returns: bool = False
    romantic_then_money: bool = False
    profile_photo_reused: bool = False


@router.post("/analyze")
def analyze(body: AccountIn, db: Session = Depends(get_db)):
    return save_scan(db, "account", f"{body.platform or ''} @{body.username or ''}", analyze_account(body.model_dump()))