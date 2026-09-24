import React, { useState } from 'react';
import { Activity, ShieldCheck, ArrowRight, AlertCircle, Sparkles, UserCheck, AlertTriangle, Heart } from 'lucide-react';
import { getPrediction } from '../api/predictionApi';
import PredictionForm from '../components/PredictionForm';
import PredictionResult from '../components/PredictionResult';

const PRESETS = {
  healthy: {
    label: 'Healthy Profile',
    icon: UserCheck,
    data: { age_years: 28, gender: 1, height: 168, weight: 58, ap_hi: 110, ap_lo: 70, cholesterol: 1, gluc: 1, smoke: 0, alco: 0, active: 1 }
  },
  borderline: {
    label: 'Moderate Profile',
    icon: Activity,
    data: { age_years: 52, gender: 2, height: 172, weight: 80, ap_hi: 135, ap_lo: 88, cholesterol: 2, gluc: 1, smoke: 0, alco: 0, active: 1 }
  },
  highRisk: {
    label: 'High Risk Profile',
    icon: AlertTriangle,
    data: { age_years: 62, gender: 2, height: 165, weight: 92, ap_hi: 165, ap_lo: 105, cholesterol: 3, gluc: 2, smoke: 1, alco: 1, active: 0 }
  }
};

const INITIAL_FORM = PRESETS.borderline.data;

function getErrorMessage(err) {
  if (!navigator.onLine || err.message === 'Failed to fetch' || err.message === 'Unable to connect to the prediction service.') {
    return 'Unable to reach the ML prediction service. Please ensure the backend is active (either local port 8000 or the live Render service).';
  }
  if (err.message === 'MODEL_ERROR') {
    return 'The machine learning engine encountered an internal calculation error. Please retry.';
  }
  if (err.message && err.message.startsWith('Validation error:')) {
    return 'Invalid input data. Please verify all clinical metrics fall within reasonable physiological ranges.';
  }
  return err.message || 'Unable to generate prediction. Please check your inputs and try again.';
}

function validate(formData) {
  const errors = {};
  if (formData.age_years < 18 || formData.age_years > 100) errors.age_years = 'Age must be between 18 and 100.';
  if (formData.height < 100 || formData.height > 220) errors.height = 'Height must be between 100 and 220 cm.';
  if (formData.weight < 30 || formData.weight > 200) errors.weight = 'Weight must be between 30 and 200 kg.';
  if (formData.ap_hi < 60 || formData.ap_hi > 240) errors.ap_hi = 'Must be between 60 and 240.';
  if (formData.ap_lo < 40 || formData.ap_lo > 140) errors.ap_lo = 'Must be between 40 and 140.';
  if (formData.ap_hi <= formData.ap_lo) errors.ap_lo = 'Systolic must be higher than Diastolic.';
  return errors;
}

export default function Home() {
  const [formData, setFormData] = useState(INITIAL_FORM);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [validationErrors, setValidationErrors] = useState({});

  const applyPreset = (presetKey) => {
    setFormData(PRESETS[presetKey].data);
    setValidationErrors({});
    setError(null);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: parseFloat(value) }));
    if (validationErrors[name]) {
      setValidationErrors((prev) => { const n = { ...prev }; delete n[name]; return n; });
    }
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setError(null);

    const errors = validate(formData);
    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      return;
    }
    setValidationErrors({});

    setLoading(true);
    
    try {
      const data = await getPrediction(formData);
      setResult(data);
      setTimeout(() => {
        document.getElementById('prediction-result')?.scrollIntoView({ behavior: 'smooth' });
      }, 150);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {/* Hero Banner */}
      <section className="hero-banner">
        <div className="hero-pill">
          <Sparkles size={14} /> Ensemble Machine Learning System
        </div>
        
        <h1 className="hero-title">
          Next-Gen <span>Cardiovascular Risk</span> Stratification
        </h1>
        
        <p className="hero-subtitle">
          Leverage a multi-stage stacking classifier combining XGBoost, LightGBM, and HistGradientBoosting to analyze clinical parameters and calculate heart disease probability.
        </p>

        <div className="hero-actions">
          <button 
            className="btn-primary" 
            onClick={() => document.getElementById('assessment-card')?.scrollIntoView({ behavior: 'smooth' })}
          >
            Start Assessment <ArrowRight size={18} />
          </button>
        </div>

        <div className="hero-metrics">
          <div className="hero-metric-item">
            <span className="hero-metric-label">Model Architecture</span>
            <span className="hero-metric-val">Stacking Ensemble</span>
          </div>
          <div className="hero-metric-item">
            <span className="hero-metric-label">Validation ROC-AUC</span>
            <span className="hero-metric-val">0.8048</span>
          </div>
          <div className="hero-metric-item">
            <span className="hero-metric-label">Training Dataset</span>
            <span className="hero-metric-val">68,640 Patients</span>
          </div>
          <div className="hero-metric-item">
            <span className="hero-metric-label">Cross-Validation</span>
            <span className="hero-metric-val">Repeated Stratified</span>
          </div>
        </div>
      </section>

      {/* Quick Demo Presets */}
      <div className="presets-bar">
        <span className="presets-label">Quick Demo Profiles:</span>
        {Object.entries(PRESETS).map(([key, preset]) => {
          const IconComponent = preset.icon;
          return (
            <button
              key={key}
              type="button"
              className="preset-btn"
              onClick={() => applyPreset(key)}
            >
              <IconComponent size={14} />
              {preset.label}
            </button>
          );
        })}
      </div>

      {/* Main Assessment Form */}
      <section id="assessment-card" className="card">
        <div className="card-header">
          <h2 className="card-title">
            <Activity size={22} color="var(--color-primary)" />
            Clinical Biomarkers & Lifestyle Metrics
          </h2>
          <p className="card-subtitle">
            Provide patient diagnostic readings to generate an instant risk stratification report.
          </p>
        </div>

        <PredictionForm
          formData={formData}
          onChange={handleChange}
          onSubmit={handlePredict}
          loading={loading}
          validationErrors={validationErrors}
        />
      </section>

      {/* API Error Message */}
      {error && (
        <div className="alert-error" role="alert">
          <AlertCircle size={22} style={{ flexShrink: 0, marginTop: '2px' }} />
          <div>
            <strong>Prediction Service Notice</strong>
            <p style={{ marginTop: '0.25rem', fontSize: '0.9rem' }}>{error}</p>
          </div>
        </div>
      )}

      {/* Prediction Result */}
      {result ? (
        <div id="prediction-result">
          <PredictionResult result={result} formData={formData} />
        </div>
      ) : !loading && !error && (
        <div className="empty-state">
          <Heart size={42} className="empty-state-icon" />
          <h3 style={{ color: 'var(--text-main)', fontSize: '1.15rem', marginBottom: '0.35rem' }}>
            Assessment Ready
          </h3>
          <p>Complete the patient metrics above or choose a demo profile to compute the cardiovascular risk probability.</p>
        </div>
      )}
    </div>
  );
}
