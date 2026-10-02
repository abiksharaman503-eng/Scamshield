"""Text cleaning + privacy redaction. Redact BEFORE anything is stored or logged."""
import re

URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"')]+|\b[a-z0-9-]+(?:\.[a-z0-9-]+)+/[^\s<>\"')]*", re.I)
_OTP_CTX = re.compile(r"(otp|code|pin|cvv|passcode)([^0-9]{0,15})(\d{4,8})", re.I)
_CARD = re.compile(r"\b(?:\d[ -]?){13,19}\b")
_AADHAAR = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")


def extract_urls(text: str) -> list[str]:
    seen, out = set(), []
    for m in URL_RE.findall(text or ""):
        m = m.rstrip(".,;:!?")
        if m.lower() not in seen:
            seen.add(m.lower())
            out.append(m)
    return out


def redact(text: str) -> str:
    text = _OTP_CTX.sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]", text or "")
    text = _CARD.sub("[CARD REDACTED]", text)
    text = _AADHAAR.sub("[ID REDACTED]", text)
    return text


def clean_text(text: str) -> str:
    text = URL_RE.sub(" URL ", text or "")
    text = re.sub(r"\d{4,}", " NUM ", text)
    return re.sub(r"\s+", " ", text).strip().lower()