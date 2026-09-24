import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_loaded" in data

def test_predict_standard_patient():
    sample_patient = {
        "age_years": 55,
        "gender": 2,
        "height": 172.0,
        "weight": 85.0,
        "ap_hi": 140.0,
        "ap_lo": 90.0,
        "cholesterol": 2,
        "gluc": 1,
        "smoke": 0,
        "alco": 0,
        "active": 1
    }
    response = client.post("/predict", json=sample_patient)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "has_cardio_disease" in data
    assert "risk_level" in data
    assert "bmi" in data
    assert isinstance(data["prediction"], float)
    assert 0.0 <= data["prediction"] <= 1.0

def test_predict_low_risk_patient():
    healthy_patient = {
        "age_years": 25,
        "gender": 1,
        "height": 165.0,
        "weight": 55.0,
        "ap_hi": 110.0,
        "ap_lo": 70.0,
        "cholesterol": 1,
        "gluc": 1,
        "smoke": 0,
        "alco": 0,
        "active": 1
    }
    response = client.post("/predict", json=healthy_patient)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] < 0.50
    assert data["has_cardio_disease"] is False

def test_predict_high_risk_patient():
    high_risk_patient = {
        "age_years": 64,
        "gender": 2,
        "height": 168.0,
        "weight": 98.0,
        "ap_hi": 170.0,
        "ap_lo": 110.0,
        "cholesterol": 3,
        "gluc": 3,
        "smoke": 1,
        "alco": 1,
        "active": 0
    }
    response = client.post("/predict", json=high_risk_patient)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] >= 0.50
    assert data["has_cardio_disease"] is True
    assert data["risk_level"] == "high"

def test_predict_bmi_autocalculation():
    patient_without_bmi = {
        "age_years": 45,
        "gender": 1,
        "height": 160.0,
        "weight": 64.0,
        "ap_hi": 120.0,
        "ap_lo": 80.0,
        "cholesterol": 1,
        "gluc": 1,
        "smoke": 0,
        "alco": 0,
        "active": 1
    }
    response = client.post("/predict", json=patient_without_bmi)
    assert response.status_code == 200
    data = response.json()
    # 64 / (1.6^2) = 25.0
    assert round(data["bmi"], 1) == 25.0

if __name__ == "__main__":
    test_health_check()
    test_predict_standard_patient()
    test_predict_low_risk_patient()
    test_predict_high_risk_patient()
    test_predict_bmi_autocalculation()
    print("All API tests passed successfully!")
