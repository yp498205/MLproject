import json
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "processed" / "cardio_cleaned.csv"
MODEL_PATH = BASE_DIR / "models" / "model.json"

def train():
    if not DATA_PATH.exists():
        from training.preprocess import run_preprocessing
        run_preprocessing()

    df = pd.read_csv(DATA_PATH, sep=";")

    feature_cols = [
        'age_years', 'gender', 'height', 'weight', 'bmi',
        'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
        'smoke', 'alco', 'active'
    ]

    X = df[feature_cols]
    y = df['cardio']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    accuracy = float(accuracy_score(y_test, y_pred))

    model_data = {
        "model_type": "LogisticRegression",
        "feature_cols": feature_cols,
        "accuracy": accuracy,
        "intercept": float(model.intercept_[0]),
        "coefficients": model.coef_[0].tolist(),
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist()
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "w") as f:
        json.dump(model_data, f, indent=2)

    print(f"Logistic Regression model trained. Accuracy: {accuracy * 100:.2f}%")
    print(f"Saved model to: {MODEL_PATH}")

if __name__ == "__main__":
    train()
