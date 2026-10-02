"""Social-media / seller profile heuristics."""
import re
from .risk_engine import sig, combine


def analyze_account(p: dict) -> dict:
    s = []
    age = p.get("account_age_days")
    followers, following = p.get("followers"), p.get("following")
    bio = (p.get("bio") or "") + " " + (p.get("display_name") or "")

    if age is not None and age < 30:
        s.append(sig("new_account", 0.3, f"The account is only {age} days old."))
    if followers is not None and following is not None and following > 20 and followers / max(following, 1) < 0.05:
        s.append(sig("follow_ratio", 0.25, "It follows many accounts but has very few followers."))
    if p.get("post_count") is not None and p["post_count"] < 3:
        s.append(sig("few_posts", 0.2, "The account has almost no posts."))
    if p.get("has_profile_photo") is False:
        s.append(sig("no_photo", 0.15, "There's no profile photo."))
    if p.get("asked_for_money"):
        s.append(sig("asked_money", 0.5, "This account asked you for money or gift cards."))
    if p.get("moved_to_private_chat"):
        s.append(sig("off_platform", 0.35, "It pushed you to continue on WhatsApp, Telegram or another private app."))
    if p.get("claims_investment_returns"):
        s.append(sig("investment", 0.45, "It promotes guaranteed investment returns."))
    if p.get("romantic_then_money"):
        s.append(sig("romance", 0.5, "A quick romance followed by requests for money is a classic romance scam."))
    if re.search(r"\b(dm (me )?(for|to)|whatsapp|telegram|crypto|forex|loan|investment|profit)\b", bio, re.I):
        s.append(sig("bio_keywords", 0.25, "The profile pushes private messages, crypto, loans or investments."))
    if p.get("profile_photo_reused"):
        s.append(sig("reused_photo", 0.5, "Its profile photo appears elsewhere under a different name."))
    return combine(s)