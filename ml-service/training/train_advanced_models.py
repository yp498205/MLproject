from pathlib import Path
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_validate, RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    StackingClassifier
)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

try:
    from xgboost import XGBClassifier
except ImportError:
    XGBClassifier = None

try:
    from lightgbm import LGBMClassifier
except ImportError:
    LGBMClassifier = None

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
    
from api.utils import FeatureEngineer

DATA_PATH = BASE_DIR / "dataset" / "processed" / "cardio_cleaned.csv"
BEST_MODEL_PATH = BASE_DIR / "models" / "best_model.joblib"

def evaluate_thresholds(y_true, y_probs):
    print("\nThreshold Analysis (Test Set):")
    best_acc, best_thresh = 0, 0.5
    for thresh in np.arange(0.2, 0.81, 0.01):
        preds = (y_probs >= thresh).astype(int)
        acc = accuracy_score(y_true, preds)
        if acc > best_acc:
            best_acc = acc
            best_thresh = thresh
        if round(thresh, 2) in [0.3, 0.4, 0.5, 0.6]:
            rec = recall_score(y_true, preds)
            prec = precision_score(y_true, preds)
            print(f"  Threshold {thresh:.2f} -> Acc: {acc:.4f}, Prec: {prec:.4f}, Recall: {rec:.4f}")
    
    print(f"\nBest threshold for Accuracy: {best_thresh:.2f} (Acc: {best_acc:.4f})")

def main():
    if not DATA_PATH.exists():
        from training.preprocess import run_preprocessing
        run_preprocessing()

    print("Loading cleaned dataset...")
    df = pd.read_csv(DATA_PATH, sep=";")
    
    feature_cols = [
        'age_years', 'gender', 'height', 'weight', 'bmi',
        'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
        'smoke', 'alco', 'active'
    ]

    X = df[feature_cols]
    y = df['cardio']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    rskf = RepeatedStratifiedKFold(n_splits=3, n_repeats=2, random_state=42)

    feature_engineer = FeatureEngineer()
    scaler = StandardScaler()
    
    models_to_evaluate = {
        "HistGradientBoosting": HistGradientBoostingClassifier(random_state=42, max_iter=100, max_depth=5)
    }
    
    estimators = []
    if XGBClassifier is not None:
        xgb = XGBClassifier(random_state=42, n_estimators=100, max_depth=5, learning_rate=0.1, eval_metric='logloss')
        models_to_evaluate["XGBoost"] = xgb
        estimators.append(('xgb', xgb))
        
    if LGBMClassifier is not None:
        lgbm = LGBMClassifier(random_state=42, n_estimators=100, max_depth=5, learning_rate=0.1, verbose=-1)
        models_to_evaluate["LightGBM"] = lgbm
        estimators.append(('lgbm', lgbm))
        
    estimators.append(('hgb', models_to_evaluate["HistGradientBoosting"]))
    
    stacking_clf = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression(), cv=3)
    models_to_evaluate["Stacking Ensemble"] = stacking_clf
    
    scoring = ['accuracy', 'roc_auc']
    comparison_data = []
    trained_pipelines = {}
    
    print("\nModel Comparison (Repeated Cross-Validation)")
    print("-" * 50)
    for name, model in models_to_evaluate.items():
        pipeline = Pipeline([
            ('engineer', feature_engineer),
            ('scaler', scaler),
            ('classifier', model)
        ])
        
        cv_results = cross_validate(pipeline, X_train, y_train, cv=rskf, scoring=scoring)
        
        mean_acc = np.mean(cv_results['test_accuracy'])
        std_acc = np.std(cv_results['test_accuracy'])
        mean_auc = np.mean(cv_results['test_roc_auc'])
        std_auc = np.std(cv_results['test_roc_auc'])
        
        comparison_data.append({
            "Model": name,
            "CV Mean Acc": f"{mean_acc:.4f} ±{std_acc:.4f}",
            "CV Mean AUC": f"{mean_auc:.4f} ±{std_auc:.4f}",
            "Raw Mean AUC": mean_auc
        })
        
        pipeline.fit(X_train, y_train)
        trained_pipelines[name] = pipeline
        
        print(f"{name}: Acc {mean_acc:.4f}, AUC {mean_auc:.4f}")

    summary_df = pd.DataFrame(comparison_data)
    display_df = summary_df.drop(columns=['Raw Mean AUC'])
    print("\n" + "=" * 90)
    print(" REPEATED CV MODEL COMPARISON SUMMARY")
    print("=" * 90)
    print(display_df.to_string(index=False))
    
    best_name = max(comparison_data, key=lambda x: x['Raw Mean AUC'])['Model']
    best_pipeline = trained_pipelines[best_name]
    
    print(f"\nSelected model: {best_name}")
    
    test_pred = best_pipeline.predict(X_test)
    test_pred_proba = best_pipeline.predict_proba(X_test)[:, 1]
    
    test_acc = accuracy_score(y_test, test_pred)
    test_prec = precision_score(y_test, test_pred)
    test_rec = recall_score(y_test, test_pred)
    test_f1 = f1_score(y_test, test_pred)
    test_auc = roc_auc_score(y_test, test_pred_proba)
    
    print("\nFinal test-set results:")
    print(f"  Accuracy:  {test_acc:.4f}")
    print(f"  Precision: {test_prec:.4f}")
    print(f"  Recall:    {test_rec:.4f}")
    print(f"  F1:        {test_f1:.4f}")
    print(f"  ROC-AUC:   {test_auc:.4f}")
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, test_pred))
    
    evaluate_thresholds(y_test, test_pred_proba)
    
    BEST_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline, BEST_MODEL_PATH)
    print(f"\nBest model pipeline ({best_name}) saved to {BEST_MODEL_PATH}")

if __name__ == "__main__":
    main()
