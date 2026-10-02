"""Train the text and URL models.

    python train.py

Data (put your own real datasets in ./dataset/ for real accuracy):
  dataset/messages.csv   columns: text,label     (label: 1 = scam, 0 = legitimate)
  dataset/urls.csv       columns: url,label      (label: 1 = phishing, 0 = benign)
Suggested public sources: UCI SMS Spam Collection, PhishTank / OpenPhish (phishing URLs), Tranco list (benign URLs).
If the CSVs are missing, a tiny SEED set is used so the pipeline runs end to end. It is NOT good enough for production.
"""
import csv
import sys
from pathlib import Path

import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "backend"))
from ml.features import url_features          # noqa: E402
from ml.preprocessing import clean_text       # noqa: E402

OUT = ROOT / "saved_models"
OUT.mkdir(exist_ok=True)

SEED_MSGS = [
    ("Your SBI account will be blocked today. Update KYC now at http://sbi-kyc-verify.top", 1),
    ("Congratulations! You have won Rs 25,00,000 in lucky draw. Share OTP to claim prize", 1),
    ("Urgent: your parcel is held at customs. Pay Rs 49 fee at http://track-parcel.xyz", 1),
    ("Work from home, earn 5000 per day. Just like and review videos. Message on Telegram", 1),
    ("This is CBI. A warrant is issued in your name. Join video call and transfer fine immediately", 1),
    ("Install this APK to receive your electricity refund. Your power will be cut tonight", 1),
    ("Guaranteed returns! Double your money in 7 days with our crypto signals", 1),
    ("Your Netflix payment failed. Verify your card at http://netflix-billing-help.click within 2 hours", 1),
    ("Dear customer share your OTP to complete refund of Rs 1999", 1),
    ("We noticed a login to your account from a new device. Confirm now or account will be suspended", 1),
    ("Install AnyDesk so our executive can fix your bank issue", 1),
    ("Hi, are we still meeting for lunch tomorrow at 1?", 0),
    ("Your OTP for login is 482913. Do not share it with anyone.", 0),
    ("Your order #4432 has shipped and will arrive on Friday.", 0),
    ("Reminder: dentist appointment on Monday at 10 AM.", 0),
    ("Rs 500 debited from your account for grocery purchase. Available balance is 12,300.", 0),
    ("Happy birthday! Let's catch up this weekend.", 0),
    ("Meeting moved to 3 PM. Agenda attached in the calendar invite.", 0),
    ("Your electricity bill for March is generated. Pay through the official app before the due date.", 0),
    ("Thanks for your payment. Your receipt is attached.", 0),
    ("Can you send me the project report by evening?", 0),
    ("Your flight is on time. Check-in opens 24 hours before departure.", 0),
]
SEED_URLS = [
    ("http://sbi-kyc-verify.top/login", 1), ("http://paypal-secure-login.xyz/verify", 1),
    ("http://192.168.44.12/bank/update.php", 1), ("http://amaz0n-refund.click/claim", 1),
    ("https://hdfc-netbanking-unlock.cyou/otp", 1), ("http://bit.ly/3xZfree", 1),
    ("http://track-parcel.xyz/pay", 1), ("http://secure-account-update.tk/signin", 1),
    ("http://netflix-billing-help.click/card", 1), ("http://free-gift-reward.top/claim/now", 1),
    ("http://phonepe-kyc.work/verify-account", 1), ("http://login.microsoft.verify-user.ml/", 1),
    ("https://www.google.com/search?q=weather", 0), ("https://en.wikipedia.org/wiki/Cat", 0),
    ("https://www.amazon.in/dp/B08N5WRWNW", 0), ("https://github.com/python/cpython", 0),
    ("https://www.hdfcbank.com/personal", 0), ("https://www.irctc.co.in/nget/train-search", 0),
    ("https://news.ycombinator.com/", 0), ("https://www.flipkart.com/mobiles", 0),
    ("https://stackoverflow.com/questions/1", 0), ("https://www.bbc.com/news", 0),
]


def load(path, col):
    if not path.exists():
        return None
    with open(path, newline="", encoding="utf-8") as f:
        rows = [(r[col], int(r["label"])) for r in csv.DictReader(f)]
    print(f"loaded {len(rows)} rows from {path.name}")
    return rows


def report(name, model, X, y):
    strat = y if min(y.count(0), y.count(1)) >= 2 else None
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=strat)
    model.fit(Xtr, ytr)
    print(f"\n== {name} ==")
    print(classification_report(yte, model.predict(Xte), zero_division=0))
    model.fit(X, y)      # refit on everything for the saved model


msgs = load(ROOT / "dataset" / "messages.csv", "text") or SEED_MSGS
urls = load(ROOT / "dataset" / "urls.csv", "url") or SEED_URLS

X, y = [clean_text(t) for t, _ in msgs], [l for _, l in msgs]
text_model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True),
                           LogisticRegression(max_iter=1000, class_weight="balanced"))
report("text model", text_model, X, y)
joblib.dump(text_model, OUT / "text_model.joblib")

X, y = [url_features(u) for u, _ in urls], [l for _, l in urls]
url_model = GradientBoostingClassifier(random_state=42)
report("url model", url_model, X, y)
joblib.dump(url_model, OUT / "url_model.joblib")
print("\nsaved models to", OUT)