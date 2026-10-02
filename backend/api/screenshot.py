from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from database.database import get_db
from ml.preprocessing import redact
from services.nlp_analyzer import analyze_message
from services.ocr_service import extract_text, decode_qr
from services.url_analyzer import analyze_url
from .url import save_scan

router = APIRouter(prefix="/api/screenshot", tags=["screenshot"])
MAX_BYTES = 8 * 1024 * 1024


@router.post("/analyze")
async def analyze(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(400, "Please upload an image file.")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "Image is too large. The limit is 8 MB.")

    qr = decode_qr(data)
    text = extract_text(data)
    if not text and not qr:
        raise HTTPException(422, "We couldn't read any text or QR code in this image. Try a sharper, cropped screenshot.")

    result = analyze_message(text) if text else analyze_url(qr)
    if qr:
        qr_res = analyze_url(qr) if qr.lower().startswith(("http", "www")) or "." in qr else None
        result["qr"] = {"payload": qr, "analysis": qr_res}
        if qr_res and qr_res["score"] > result["score"]:
            result = {**result, "score": qr_res["score"], "level": qr_res["level"], "verdict": qr_res["verdict"]}
            result["reasons"] = ["The QR code leads to a suspicious address."] + result["reasons"]
    result["extracted_text"] = redact(text)[:2000]      # never return raw OTP/card numbers
    return save_scan(db, "screenshot", text or qr or "", result)