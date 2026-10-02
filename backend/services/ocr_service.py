"""
Screenshot -> text (OCR) and QR payload.

Uses Tesseract OCR for text extraction and OpenCV for QR decoding.
"""

import io

from PIL import Image, ImageOps, ImageEnhance, ImageFilter

try:
    import pytesseract
except ImportError:
    pytesseract = None

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


# ---------------------------------------------------------
# Tesseract configuration
# ---------------------------------------------------------

if pytesseract is not None:
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


# ---------------------------------------------------------
# OCR
# ---------------------------------------------------------

def extract_text(image_bytes: bytes) -> str:
    """Extract readable text from an uploaded screenshot."""

    if pytesseract is None:
        print("OCR error: pytesseract is not installed.")
        return ""

    if not image_bytes:
        print("OCR error: empty image.")
        return ""

    try:
        # Load image
        image = Image.open(
            io.BytesIO(image_bytes)
        )

        # Fix EXIF rotation
        image = ImageOps.exif_transpose(image)

        # Convert to RGB
        image = image.convert("RGB")

        # Get dimensions
        width, height = image.size

        # Upscale small screenshots
        if width < 1800:
            scale = 2

            image = image.resize(
                (
                    width * scale,
                    height * scale,
                ),
                Image.Resampling.LANCZOS,
            )

        # Grayscale
        gray = ImageOps.grayscale(image)

        # Automatic contrast
        gray = ImageOps.autocontrast(gray)

        # Increase contrast
        gray = ImageEnhance.Contrast(
            gray
        ).enhance(1.8)

        # Sharpen
        gray = gray.filter(
            ImageFilter.SHARPEN
        )

        # Store OCR attempts
        results = []

        # Try multiple page segmentation modes
        configs = [
            "--oem 3 --psm 6",
            "--oem 3 --psm 11",
            "--oem 3 --psm 12",
        ]

        for config in configs:
            try:
                text = pytesseract.image_to_string(
                    gray,
                    config=config,
                ).strip()

                if text:
                    results.append(text)

            except Exception as exc:
                print(
                    f"OCR attempt failed: {exc}"
                )

        # Try thresholded image
        try:
            threshold = gray.point(
                lambda pixel:
                255 if pixel > 160 else 0
            )

            text = pytesseract.image_to_string(
                threshold,
                config="--oem 3 --psm 6",
            ).strip()

            if text:
                results.append(text)

        except Exception as exc:
            print(
                f"OCR threshold failed: {exc}"
            )

        # No text found
        if not results:
            print(
                "OCR completed but no readable text was found."
            )
            return ""

        # Choose longest result
        best_text = max(
            results,
            key=len,
        ).strip()

        print("OCR extracted text:")
        print(best_text)

        return best_text

    except Exception as exc:
        print(f"OCR error: {exc}")
        return ""


# ---------------------------------------------------------
# QR decoder
# ---------------------------------------------------------

def decode_qr(image_bytes: bytes) -> str | None:
    """Decode a QR code from the uploaded image."""

    if cv2 is None or np is None:
        print(
            "QR decoder unavailable: "
            "OpenCV/numpy not installed."
        )
        return None

    if not image_bytes:
        return None

    try:
        # Convert bytes to numpy array
        arr = np.frombuffer(
            image_bytes,
            dtype=np.uint8,
        )

        # Decode image
        image = cv2.imdecode(
            arr,
            cv2.IMREAD_COLOR,
        )

        if image is None:
            print(
                "QR decoder could not read image."
            )
            return None

        detector = cv2.QRCodeDetector()

        # Normal image
        data, _, _ = detector.detectAndDecode(
            image
        )

        if data:
            print(
                f"QR payload detected: {data}"
            )
            return data.strip()

        # Grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

        data, _, _ = detector.detectAndDecode(
            gray
        )

        if data:
            print(
                f"QR payload detected: {data}"
            )
            return data.strip()

        # Enlarged image
        height, width = gray.shape

        if width < 1500:
            enlarged = cv2.resize(
                gray,
                (
                    width * 2,
                    height * 2,
                ),
                interpolation=cv2.INTER_CUBIC,
            )

            data, _, _ = detector.detectAndDecode(
                enlarged
            )

            if data:
                print(
                    f"QR payload detected: {data}"
                )
                return data.strip()

        print("No QR code detected.")

        return None

    except Exception as exc:
        print(
            f"QR decoding error: {exc}"
        )
        return None