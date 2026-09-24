import json
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "processed" / "cardio_cleaned.csv"
MODEL_PATH = BASE_DIR / "models" / "decision_tree.joblib"
META_PATH = BASE_DIR / "models" / "decision_tree.json"

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

    model = DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = float(accuracy_score(y_test, y_pred))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    importances = {col: float(imp) for col, imp in zip(feature_cols, model.feature_importances_)}
    meta_data = {
        "model_type": "DecisionTreeClassifier",
        "feature_cols": feature_cols,
        "max_depth": 5,
        "min_samples_split": 10,
        "accuracy": accuracy,
        "feature_importances": importances
    }
    with open(META_PATH, "w") as f:
        json.dump(meta_data, f, indent=2)

    print(f"Decision Tree model trained. Accuracy: {accuracy * 100:.2f}%")
    print(f"Saved joblib model to: {MODEL_PATH}")
    print(f"Saved metadata to: {META_PATH}")

if __name__ == "__main__":
    train()
