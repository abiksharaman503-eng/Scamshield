"""Message analysis: pattern rules (explainable) + optional trained text model."""
import re
from ml.model import predict_text
from ml.preprocessing import extract_urls
from .risk_engine import sig, combine
from .url_analyzer import analyze_url

RULES = [
    ("otp_request", 0.55, r"\b(share|send|tell|give|enter|provide)\b.{0,30}\b(otp|pin|cvv|password|passcode)\b",
     "It asks you to share an OTP, PIN or password. Real companies never ask for these."),
    ("urgency", 0.3, r"\b(urgent|immediately|within \d+ ?(hours?|hrs?|minutes?|mins?)|last chance|expires? (today|soon)|act now|final notice)\b",
     "It pushes you to act fast, which is a pressure tactic."),
    ("account_threat", 0.4, r"\b(account|card|sim|number|upi|wallet).{0,25}\b(blocked|suspended|deactivated|closed|frozen|expire[ds]?)\b",
     "It threatens to block or close an account unless you act."),
    ("kyc", 0.35, r"\b(kyc|pan card|aadhaar|aadhar).{0,30}\b(update|verify|expire|pending|mandatory)\b",
     "It asks for a KYC or ID update through a message, a very common scam."),
    ("prize", 0.5, r"\b(you (have )?won|lottery|lucky (draw|winner)|prize|congratulations.{0,30}(won|selected)|claim (your )?(reward|gift|prize))\b",
     "It says you've won something you never entered for."),
    ("authority_threat", 0.5, r"\b(arrest|police|cbi|customs|narcotics|warrant|court|digital arrest|legal action)\b.{0,60}\b(pay|transfer|verify|fine|video call)\b",
     "It threatens legal trouble and asks for payment or a video call. Real agencies don't do this."),
    ("payment_ask", 0.35, r"\b(pay|transfer|send)\b.{0,30}(₹|rs\.?|inr|\$|usd|upi|gift ?cards?|bitcoin|usdt|crypto)",
     "It asks you to send money or gift cards."),
    ("job_scam", 0.4, r"\b(work from home|part[- ]time job|earn (up to )?(₹|rs\.?|\$)?\d+.{0,15}(daily|per day|weekly)|like (and|&) (subscribe|review)|task[- ]based)\b",
     "It offers easy money for simple tasks, a typical job scam."),
    ("remote_access", 0.55, r"\b(anydesk|teamviewer|quicksupport|rustdesk|screen ?share)\b",
     "It asks you to install a remote-access app, which lets a scammer control your phone."),
    ("apk", 0.45, r"\.apk\b|install (this|the) (app|apk)",
     "It asks you to install an app from outside the official app store."),
    ("delivery", 0.3, r"\b(package|parcel|courier|delivery).{0,40}\b(held|failed|undelivered|customs fee|redeliver|address)\b",
     "It claims a parcel problem and asks for a fee or details."),
    ("investment", 0.4, r"\b(guaranteed returns?|double your (money|investment)|risk[- ]free|insider tip|crypto (signal|trading)|100% profit)\b",
     "It promises guaranteed or unusually high returns."),
    ("refund", 0.3, r"\b(refund|cashback|reversal).{0,30}\b(click|link|verify|scan|enter)\b",
     "It offers a refund that needs you to click, scan or enter details."),
    ("secrecy", 0.25, r"\b(don'?t tell|do not tell|keep (this )?(secret|confidential)|don'?t (call|inform) (your )?(bank|family))\b",
     "It tells you to keep this secret. Scammers isolate their targets."),
]


def analyze_message(text: str) -> dict:
    signals = []
    for name, weight, pattern, reason in RULES:
        if re.search(pattern, text, re.I | re.S):
            signals.append(sig(name, weight, reason))

    urls = extract_urls(text)
    url_results = []
    for u in urls[:5]:
        r = analyze_url(u)
        url_results.append({"url": u, "score": r["score"], "level": r["level"], "reasons": r["reasons"][:3]})
        if r["score"] >= 50:
            signals.append(sig("bad_link", min(0.7, r["score"] / 130), f"A link in the message looks suspicious: {u[:60]}"))

    result = combine(signals, ml_prob=predict_text(text))
    result["urls"] = url_results
    return result