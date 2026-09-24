from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "dataset" / "processed" / "cardio_cleaned.csv"

class LogisticRegressionScratch:
    def __init__(self, lr=0.1, iterations=1000):
        self.lr = lr
        self.iterations = iterations
        self.w = None
        self.b = 0.0

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)

        for _ in range(self.iterations):
            # Linear model z = X * w + b
            z = np.dot(X, self.w) + self.b
            y_pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

            # Gradient computation and update
            dw = np.dot(X.T, (y_pred - y)) / n_samples
            db = np.sum(y_pred - y) / n_samples

            self.w -= self.lr * dw
            self.b -= self.lr * db

    def predict(self, X):
        z = np.dot(X, self.w) + self.b
        y_pred = 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        return (y_pred >= 0.5).astype(int)

def main():
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

    X = df[feature_cols].values
    y = df['cardio'].values

    # Split and scale data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mean, std = X_train.mean(axis=0), X_train.std(axis=0)
    std = np.where(std == 0, 1.0, std)
    X_train = (X_train - mean) / std
    X_test = (X_test - mean) / std

    # Train & evaluate model
    model = LogisticRegressionScratch(lr=0.1, iterations=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = np.mean(y_pred == y_test)

    print(f"Logistic Regression (Scratch) Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    main()
