from pathlib import Path
import sys
import json
import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from api.utils import FeatureEngineer, FEATURE_COLS

MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"
DT_MODEL_PATH = BASE_DIR / "models" / "decision_tree.joblib"
LR_MODEL_PATH = BASE_DIR / "models" / "model.json"

_cached_pipeline = None

def get_pipeline():
    global _cached_pipeline
    if _cached_pipeline is not None:
        return _cached_pipeline
        
    if MODEL_PATH.exists():
        try:
            _cached_pipeline = joblib.load(MODEL_PATH)
            return _cached_pipeline
        except Exception as e:
            print(f"Error loading best_model.joblib: {e}")
            
    if DT_MODEL_PATH.exists():
        try:
            _cached_pipeline = joblib.load(DT_MODEL_PATH)
            return _cached_pipeline
        except Exception as e:
            print(f"Error loading decision_tree.joblib: {e}")
            
    return None

def predict_cardio(data: dict) -> dict:
    """
    Takes patient health parameters and produces a cardiovascular disease risk prediction.
    """
    # Safe input normalization
    cleaned_data = {}
    for col in FEATURE_COLS:
        val = data.get(col)
        if val is not None:
            try:
                cleaned_data[col] = float(val)
            except (ValueError, TypeError):
                cleaned_data[col] = 0.0
        else:
            cleaned_data[col] = 0.0

    # Auto compute BMI if missing or zero
    if cleaned_data.get('bmi', 0) <= 0:
        height = cleaned_data.get('height', 170.0)
        weight = cleaned_data.get('weight', 70.0)
        if height > 0:
            cleaned_data['bmi'] = round(weight / ((height / 100.0) ** 2), 2)
        else:
            cleaned_data['bmi'] = 24.2

    pipeline = get_pipeline()

    if pipeline is not None:
        df = pd.DataFrame([cleaned_data])
        
        try:
            if hasattr(pipeline, "predict_proba"):
                prob_array = pipeline.predict_proba(df)
                probability = float(prob_array[0, 1])
            else:
                pred = pipeline.predict(df)[0]
                probability = 1.0 if pred == 1 else 0.0
                
            prediction_class = int(pipeline.predict(df)[0])
        except Exception as e:
            # If the loaded pipeline fails, fallback to rule-based clinical scoring
            print(f"Pipeline prediction error: {e}")
            return _fallback_prediction(cleaned_data)
            
        risk_level = "low"
        if probability >= 0.50:
            risk_level = "high"
        elif probability >= 0.30:
            risk_level = "moderate"

        return {
            "prediction": float(round(probability, 4)),
            "has_cardio_disease": bool(prediction_class == 1 or probability >= 0.5),
            "risk_level": risk_level,
            "bmi": float(cleaned_data['bmi'])
        }

    # Fallback to model.json (linear parameters) if available
    if LR_MODEL_PATH.exists():
        try:
            with open(LR_MODEL_PATH, "r") as f:
                model_meta = json.load(f)
            intercept = model_meta["intercept"]
            coefs = model_meta["coefficients"]
            means = model_meta["mean"]
            scales = model_meta["scale"]
            
            x_scaled = []
            for i, col in enumerate(FEATURE_COLS):
                raw_val = cleaned_data.get(col, means[i])
                scaled_val = (raw_val - means[i]) / (scales[i] if scales[i] != 0 else 1.0)
                x_scaled.append(scaled_val)
                
            z = intercept + sum(c * x for c, x in zip(coefs, x_scaled))
            prob = float(1.0 / (1.0 + np.exp(-np.clip(z, -500, 500))))
            return {
                "prediction": float(round(prob, 4)),
                "has_cardio_disease": bool(prob >= 0.5),
                "risk_level": "high" if prob >= 0.5 else "moderate" if prob >= 0.3 else "low",
                "bmi": float(cleaned_data['bmi'])
            }
        except Exception as e:
            print(f"Error evaluating model.json: {e}")

    # Fallback: Clinical logistic formula
    return _fallback_prediction(cleaned_data)

def _fallback_prediction(cleaned_data: dict) -> dict:
    age = cleaned_data.get('age_years', 50.0)
    ap_hi = cleaned_data.get('ap_hi', 120.0)
    ap_lo = cleaned_data.get('ap_lo', 80.0)
    chol = cleaned_data.get('cholesterol', 1.0)
    bmi = cleaned_data.get('bmi', 25.0)
    smoke = cleaned_data.get('smoke', 0.0)
    active = cleaned_data.get('active', 1.0)

    score = (age - 53) * 0.05 + (ap_hi - 128) * 0.04 + (ap_lo - 81) * 0.02 + (chol - 1) * 0.4 + (bmi - 25) * 0.03
    if smoke == 1:
        score += 0.2
    if active == 0:
        score += 0.3

    prob = float(1.0 / (1.0 + np.exp(-score)))
    return {
        "prediction": float(round(prob, 4)),
        "has_cardio_disease": bool(prob >= 0.5),
        "risk_level": "high" if prob >= 0.5 else "moderate" if prob >= 0.3 else "low",
        "bmi": float(bmi)
    }
