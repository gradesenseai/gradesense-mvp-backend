from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

APP_ENV = os.getenv("APP_ENV", "production")
MAX_IMAGE_MB = float(os.getenv("MAX_IMAGE_MB", "8"))
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}

app = FastAPI(title="GradeSense API", version="0.1.0")

origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
allow_all = origins == ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

def _validate_image(file: UploadFile):
    if file is None:
        raise HTTPException(status_code=400, detail="Missing image")
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Only JPEG/PNG supported")
    size_header = file.headers.get("content-length") or file.headers.get("Content-Length")
    if size_header:
        try:
            mb = int(size_header) / (1024 * 1024)
            if mb > MAX_IMAGE_MB:
                raise HTTPException(status_code=413, detail=f"Image too large (> {MAX_IMAGE_MB} MB)")
        except Exception:
            pass

@app.post("/estimate")
async def estimate(front: UploadFile = File(...), back: UploadFile = File(...)):
    _validate_image(front)
    _validate_image(back)

    subgrades = {"centering": 8, "corners": 8, "edges": 8, "surface": 8}
    overall = 8.0
    notes = ["MVP placeholder: calibration incoming"]

    return {"overall": overall, "subgrades": subgrades, "notes": notes}