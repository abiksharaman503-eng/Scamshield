"""Loads trained models if present. If not, callers fall back to rules only."""
from pathlib import Path
import joblib
from .features import url_features
from .preprocessing import clean_text

MODEL_DIR = Path(__file__).resolve().parents[2] / "ml" / "saved_models"
_cache: dict = {}


def _load(name: str):
    if name not in _cache:
        path = MODEL_DIR / name
        _cache[name] = joblib.load(path) if path.exists() else None
    return _cache[name]


def predict_text(text: str):
    """Probability the message is a scam, or None if no model is trained."""
    m = _load("text_model.joblib")
    return float(m.predict_proba([clean_text(text)])[0][1]) if m else None


def predict_url(url: str):
    m = _load("url_model.joblib")
    return float(m.predict_proba([url_features(url)])[0][1]) if m else None