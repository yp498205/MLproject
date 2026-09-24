from pathlib import Path
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from api.predict import predict_cardio, get_pipeline

app = FastAPI(
    title="CardioSense Risk Prediction API",
    description="Machine learning API for cardiovascular disease risk prediction using Stacking Ensemble model.",
    version="1.0.0"
)

# Enable CORS for frontend integration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    age_years: float = Field(..., ge=1, le=120, description="Age in years")
    gender: int = Field(..., ge=1, le=2, description="1: Female, 2: Male")
    height: float = Field(..., ge=50, le=250, description="Height in cm")
    weight: float = Field(..., ge=20, le=300, description="Weight in kg")
    ap_hi: float = Field(..., ge=40, le=300, description="Systolic blood pressure (mmHg)")
    ap_lo: float = Field(..., ge=20, le=200, description="Diastolic blood pressure (mmHg)")
    cholesterol: int = Field(..., ge=1, le=3, description="1: Normal, 2: Above normal, 3: Well above normal")
    gluc: int = Field(..., ge=1, le=3, description="1: Normal, 2: Above normal, 3: Well above normal")
    smoke: int = Field(0, ge=0, le=1, description="0: Non-smoker, 1: Smoker")
    alco: int = Field(0, ge=0, le=1, description="0: Non-drinker, 1: Drinker")
    active: int = Field(1, ge=0, le=1, description="0: Inactive, 1: Active")
    bmi: Optional[float] = None

class PredictionResponse(BaseModel):
    prediction: float
    has_cardio_disease: bool
    risk_level: str
    bmi: float

@app.get("/health")
@app.get("/api/health")
def health_check():
    pipeline_loaded = get_pipeline() is not None
    return {
        "status": "healthy",
        "service": "CardioSense ML Service",
        "model_loaded": pipeline_loaded
    }

@app.post("/predict", response_model=PredictionResponse)
def predict(data: dict):
    try:
        result = predict_cardio(data)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
DIST_DIR = FRONTEND_DIR / "dist"

# Mount static dist assets if React production build is present
if DIST_DIR.exists() and (DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

@app.get("/")
def get_index():
    if (DIST_DIR / "index.html").exists():
        return FileResponse(DIST_DIR / "index.html")
    if (FRONTEND_DIR / "index.html").exists():
        return FileResponse(FRONTEND_DIR / "index.html")
    return {"message": "CardioSense ML API is running. Visit /docs for documentation."}

@app.get("/style.css")
def get_css():
    if (FRONTEND_DIR / "style.css").exists():
        return FileResponse(FRONTEND_DIR / "style.css")
    return JSONResponse(status_code=404, content={"message": "Not found"})

@app.get("/app.js")
def get_js():
    if (FRONTEND_DIR / "app.js").exists():
        return FileResponse(FRONTEND_DIR / "app.js")
    return JSONResponse(status_code=404, content={"message": "Not found"})
