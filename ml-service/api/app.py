from pathlib import Path
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from api.predict import predict_cardio, get_pipeline

app = FastAPI(
    title="CardioGuard AI — Risk Prediction API",
    description="Asynchronous machine learning API for cardiovascular disease risk stratification using a Stacking Classifier Ensemble.",
    version="1.0.0"
)

# Enable CORS for frontend integration (Vercel & Localhost)
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

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
        "service": "CardioGuard AI Backend Service",
        "model_loaded": pipeline_loaded,
        "model_type": "Stacking Classifier Ensemble (0.8048 ROC-AUC)"
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

# Mount static dist assets if React production build is present locally
if DIST_DIR.exists() and (DIST_DIR / "assets").exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

API_LANDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CardioGuard AI — ML API Service</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      background: #0f172a;
      color: #f8fafc;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }
    .card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 20px;
      padding: 2.5rem;
      max-width: 600px;
      width: 100%;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
      text-align: center;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(13, 148, 136, 0.2);
      color: #2dd4bf;
      border: 1px solid rgba(45, 212, 191, 0.3);
      padding: 0.35rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 1.25rem;
    }
    .dot {
      width: 8px;
      height: 8px;
      background: #2dd4bf;
      border-radius: 50%;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(45, 212, 191, 0.4); }
      70% { box-shadow: 0 0 0 8px rgba(45, 212, 191, 0); }
      100% { box-shadow: 0 0 0 0 rgba(45, 212, 191, 0); }
    }
    h1 {
      font-family: 'Space Grotesk', sans-serif;
      font-size: 2rem;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 0.75rem;
      letter-spacing: -0.5px;
    }
    p {
      color: #94a3b8;
      font-size: 0.95rem;
      line-height: 1.6;
      margin-bottom: 2rem;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      margin-bottom: 2rem;
      text-align: left;
    }
    .grid-item {
      background: #0f172a;
      border: 1px solid #334155;
      padding: 1rem;
      border-radius: 12px;
    }
    .grid-label {
      font-size: 0.75rem;
      color: #64748b;
      font-weight: 600;
      text-transform: uppercase;
    }
    .grid-val {
      font-size: 1.1rem;
      font-weight: 700;
      color: #38bdf8;
      margin-top: 0.2rem;
    }
    .actions {
      display: flex;
      gap: 0.75rem;
      justify-content: center;
      flex-wrap: wrap;
    }
    .btn {
      padding: 0.75rem 1.4rem;
      border-radius: 10px;
      font-weight: 600;
      font-size: 0.9rem;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s;
    }
    .btn-primary {
      background: linear-gradient(135deg, #0f766e, #4338ca);
      color: white;
      box-shadow: 0 4px 12px rgba(15, 118, 110, 0.3);
    }
    .btn-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(15, 118, 110, 0.4);
    }
    .btn-secondary {
      background: #334155;
      color: #f8fafc;
    }
    .btn-secondary:hover {
      background: #475569;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">
      <div class="dot"></div>
      Backend ML Service Live & Healthy
    </div>
    <h1>CardioGuard AI API</h1>
    <p>
      Asynchronous Machine Learning service running the Stacking Classifier Ensemble for real-time cardiovascular disease risk stratification.
    </p>

    <div class="grid">
      <div class="grid-item">
        <div class="grid-label">Active Model</div>
        <div class="grid-val">Stacking Ensemble</div>
      </div>
      <div class="grid-item">
        <div class="grid-label">Validation ROC-AUC</div>
        <div class="grid-val">0.8048</div>
      </div>
      <div class="grid-item">
        <div class="grid-label">Latency Target</div>
        <div class="grid-val">&lt; 50ms</div>
      </div>
      <div class="grid-item">
        <div class="grid-label">Trained Records</div>
        <div class="grid-val">68,640 Patients</div>
      </div>
    </div>

    <div class="actions">
      <a href="/docs" class="btn btn-primary">Open Interactive API Docs (/docs)</a>
      <a href="/health" class="btn btn-secondary">Health Status (/health)</a>
    </div>
  </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def get_index():
    if (DIST_DIR / "index.html").exists():
        return FileResponse(DIST_DIR / "index.html")
    return HTMLResponse(content=API_LANDING_HTML, status_code=200)
