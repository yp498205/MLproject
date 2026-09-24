from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "processed" / "cardio_cleaned.csv"

def evaluate():
    if not DATA_PATH.exists():
        from training.preprocess import run_preprocessing
        run_preprocessing()
        
    # Load dataset
    df = pd.read_csv(DATA_PATH, sep=";")

    feature_cols = [
        'age_years', 'gender', 'height', 'weight', 'bmi',
        'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
        'smoke', 'alco', 'active'
    ]

    X = df[feature_cols]
    y = df['cardio']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features for Logistic Regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Logistic Regression": (LogisticRegression(random_state=42, max_iter=1000), X_train_scaled, X_test_scaled),
        "Decision Tree": (DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=42), X_train, X_test)
    }

    print("=" * 60)
    print(" BASELINE MODELS EVALUATION")
    print("=" * 60)

    for name, (model, train_x, test_x) in models.items():
        model.fit(train_x, y_train)

        train_acc = accuracy_score(y_train, model.predict(train_x))
        y_pred = model.predict(test_x)
        y_prob = model.predict_proba(test_x)[:, 1] if hasattr(model, "predict_proba") else None
        test_acc = accuracy_score(y_test, y_pred)

        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob) if y_prob is not None else 0.0
        cm = confusion_matrix(y_test, y_pred)

        print(f"\n{name}:")
        print(f"  Train Accuracy : {train_acc * 100:.2f}%")
        print(f"  Test Accuracy  : {test_acc * 100:.2f}%")
        print(f"  Precision      : {prec:.4f}")
        print(f"  Recall         : {rec:.4f}")
        print(f"  F1 Score       : {f1:.4f}")
        print(f"  ROC-AUC        : {auc:.4f}")
        print(f"  Confusion Matrix:\n{cm}")

        # Overfitting check
        if (train_acc - test_acc) > 0.05:
            print("  Status: Overfitting detected")
        else:
            print("  Status: Good fit (No overfitting)")

if __name__ == "__main__":
    evaluate()
