import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

FEATURE_COLS = [
    'age_years', 'gender', 'height', 'weight', 'bmi',
    'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
    'smoke', 'alco', 'active'
]

class FeatureEngineer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        if not isinstance(X, pd.DataFrame):
            if isinstance(X, np.ndarray):
                X = pd.DataFrame(X, columns=FEATURE_COLS[:X.shape[1]])
            else:
                X = pd.DataFrame(X)
        else:
            X = X.copy()
            
        # Safe numeric calculations
        ap_hi = pd.to_numeric(X['ap_hi'], errors='coerce').fillna(120.0)
        ap_lo = pd.to_numeric(X['ap_lo'], errors='coerce').fillna(80.0)
        age_years = pd.to_numeric(X['age_years'], errors='coerce').fillna(50.0)
        weight = pd.to_numeric(X['weight'], errors='coerce').fillna(70.0)
        height = pd.to_numeric(X['height'], errors='coerce').fillna(165.0)
        bmi = pd.to_numeric(X.get('bmi', weight / ((height / 100) ** 2)), errors='coerce').fillna(25.0)
        chol = pd.to_numeric(X['cholesterol'], errors='coerce').fillna(1.0)
        gluc = pd.to_numeric(X['gluc'], errors='coerce').fillna(1.0)

        ap_lo_safe = ap_lo.replace(0, 1)
        pulse_pressure = ap_hi - ap_lo
        mean_arterial_pressure = ap_lo + (pulse_pressure / 3.0)
        bp_ratio = ap_hi / ap_lo_safe
        age_ap_hi = age_years * ap_hi
        cholesterol_gluc = chol * gluc
        bmi_age = bmi * age_years
        
        # Log transformations
        log_weight = np.log1p(np.maximum(0, weight))
        log_bmi = np.log1p(np.maximum(0, bmi))
        
        # Binning with infinite bounds to prevent NaN
        age_group = pd.cut(age_years, bins=[-np.inf, 40, 50, 60, np.inf], labels=[0, 1, 2, 3], include_lowest=True).astype(float).fillna(1.0)
        bmi_category = pd.cut(bmi, bins=[-np.inf, 18.5, 25, 30, np.inf], labels=[0, 1, 2, 3], include_lowest=True).astype(float).fillna(1.0)
        sys_bp_category = pd.cut(ap_hi, bins=[-np.inf, 120, 130, 140, np.inf], labels=[0, 1, 2, 3], include_lowest=True).astype(float).fillna(1.0)
        
        X['pulse_pressure'] = pulse_pressure
        X['mean_arterial_pressure'] = mean_arterial_pressure
        X['bp_ratio'] = bp_ratio
        X['age_ap_hi'] = age_ap_hi
        X['cholesterol_gluc'] = cholesterol_gluc
        X['bmi_age'] = bmi_age
        X['log_weight'] = log_weight
        X['log_bmi'] = log_bmi
        X['age_group'] = age_group
        X['bmi_category'] = bmi_category
        X['sys_bp_category'] = sys_bp_category
        
        return X
