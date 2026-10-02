"""Numeric URL features shared by training (ml/train.py) and inference."""
import math
import re
from urllib.parse import urlparse

SUSPICIOUS_TLDS = {"zip", "mov", "top", "xyz", "click", "link", "gq", "tk", "ml", "cf", "ga", "work",
                   "support", "country", "rest", "fit", "cam", "monster", "icu", "buzz", "cyou"}
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rb.gy", "shorturl.at", "ow.ly", "tiny.cc"}
KEYWORDS = ["login", "verify", "secure", "update", "account", "bank", "confirm", "wallet", "kyc",
            "otp", "reward", "gift", "claim", "free", "suspend", "unlock", "refund", "signin", "pay"]


def parse(url: str):
    url = url.strip()
    if not re.match(r"^[a-z][a-z0-9+.-]*://", url, re.I):
        url = "http://" + url
    return urlparse(url)


def _entropy(s: str) -> float:
    if not s:
        return 0.0
    return -sum((s.count(c) / len(s)) * math.log2(s.count(c) / len(s)) for c in set(s))


def url_features(url: str) -> list[float]:
    p = parse(url)
    host = (p.hostname or "").lower()
    labels = host.split(".")
    tld = labels[-1] if labels else ""
    full = url.lower()
    return [
        len(url), len(host), host.count("."), host.count("-"), sum(c.isdigit() for c in host),
        1.0 if "@" in url else 0.0,
        1.0 if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host) else 0.0,
        1.0 if "xn--" in host else 0.0,
        1.0 if p.scheme == "https" else 0.0,
        1.0 if tld in SUSPICIOUS_TLDS else 0.0,
        1.0 if host in SHORTENERS else 0.0,
        max(len(labels) - 2, 0),
        sum(k in full for k in KEYWORDS),
        _entropy(host), len(p.path or ""),
        1.0 if p.port else 0.0,
    ]