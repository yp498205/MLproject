import React from 'react';
import { User, Scale, Activity, Droplets, HeartHandshake, Play } from 'lucide-react';

export default function PredictionForm({ formData, onChange, onSubmit, loading, validationErrors = {} }) {
  const currentBmi = formData.height > 0 && formData.weight > 0
    ? (formData.weight / Math.pow(formData.height / 100, 2)).toFixed(1)
    : '24.2';

  const getBmiCategory = (bmi) => {
    const num = parseFloat(bmi);
    if (num < 18.5) return { label: 'Underweight', color: 'var(--color-warning)' };
    if (num < 25.0) return { label: 'Normal', color: 'var(--color-success)' };
    if (num < 30.0) return { label: 'Overweight', color: 'var(--color-warning)' };
    return { label: 'Obese', color: 'var(--color-danger)' };
  };

  const bmiCat = getBmiCategory(currentBmi);

  return (
    <form onSubmit={onSubmit} noValidate>
      {/* 1. Demographics */}
      <div className="form-section">
        <div className="form-section-header">
          <div className="form-section-icon"><User size={18} /></div>
          <h3 className="form-section-title">Patient Demographics</h3>
        </div>
        <div className="form-grid">
          <div className="form-group">
            <label className="form-label">
              Age <span className="form-unit">years</span>
            </label>
            <input
              type="number"
              name="age_years"
              className={`form-input ${validationErrors.age_years ? 'input-error' : ''}`}
              value={formData.age_years}
              onChange={onChange}
              placeholder="e.g. 55"
            />
            {validationErrors.age_years && <span className="form-error">{validationErrors.age_years}</span>}
          </div>
          <div className="form-group">
            <label className="form-label">Biological Sex</label>
            <select name="gender" className="form-select" value={formData.gender} onChange={onChange}>
              <option value={1}>Female</option>
              <option value={2}>Male</option>
            </select>
          </div>
        </div>
      </div>

      {/* 2. Body Composition */}
      <div className="form-section">
        <div className="form-section-header" style={{ justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <div className="form-section-icon"><Scale size={18} /></div>
            <h3 className="form-section-title">Body Composition</h3>
          </div>
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: bmiCat.color, background: 'white', padding: '0.25rem 0.65rem', borderRadius: 'var(--radius-full)', border: '1px solid var(--border-light)' }}>
            Calculated BMI: {currentBmi} ({bmiCat.label})
          </div>
        </div>
        <div className="form-grid">
          <div className="form-group">
            <label className="form-label">
              Height <span className="form-unit">cm</span>
            </label>
            <input
              type="number"
              name="height"
              className={`form-input ${validationErrors.height ? 'input-error' : ''}`}
              value={formData.height}
              onChange={onChange}
              placeholder="e.g. 170"
            />
            {validationErrors.height && <span className="form-error">{validationErrors.height}</span>}
          </div>
          <div className="form-group">
            <label className="form-label">
              Weight <span className="form-unit">kg</span>
            </label>
            <input
              type="number"
              name="weight"
              className={`form-input ${validationErrors.weight ? 'input-error' : ''}`}
              value={formData.weight}
              onChange={onChange}
              placeholder="e.g. 75"
            />
            {validationErrors.weight && <span className="form-error">{validationErrors.weight}</span>}
          </div>
        </div>
      </div>

      {/* 3. Hemodynamics */}
      <div className="form-section">
        <div className="form-section-header">
          <div className="form-section-icon"><Activity size={18} /></div>
          <h3 className="form-section-title">Blood Pressure Readings</h3>
        </div>
        <div className="form-grid">
          <div className="form-group">
            <label className="form-label">
              Systolic Pressure (ap_hi) <span className="form-unit">mmHg</span>
            </label>
            <input
              type="number"
              name="ap_hi"
              className={`form-input ${validationErrors.ap_hi ? 'input-error' : ''}`}
              value={formData.ap_hi}
              onChange={onChange}
              placeholder="e.g. 120"
            />
            {validationErrors.ap_hi && <span className="form-error">{validationErrors.ap_hi}</span>}
            <span className="form-hint">Optimal target: 90 – 120 mmHg</span>
          </div>
          <div className="form-group">
            <label className="form-label">
              Diastolic Pressure (ap_lo) <span className="form-unit">mmHg</span>
            </label>
            <input
              type="number"
              name="ap_lo"
              className={`form-input ${validationErrors.ap_lo ? 'input-error' : ''}`}
              value={formData.ap_lo}
              onChange={onChange}
              placeholder="e.g. 80"
            />
            {validationErrors.ap_lo && <span className="form-error">{validationErrors.ap_lo}</span>}
            <span className="form-hint">Optimal target: 60 – 80 mmHg</span>
          </div>
        </div>
      </div>

      {/* 4. Laboratory Biomarkers */}
      <div className="form-section">
        <div className="form-section-header">
          <div className="form-section-icon"><Droplets size={18} /></div>
          <h3 className="form-section-title">Metabolic Biomarkers</h3>
        </div>
        <div className="form-grid">
          <div className="form-group">
            <label className="form-label">Total Serum Cholesterol</label>
            <select name="cholesterol" className="form-select" value={formData.cholesterol} onChange={onChange}>
              <option value={1}>1 — Normal Range (&lt; 200 mg/dL)</option>
              <option value={2}>2 — Borderline / Above Normal (200-239 mg/dL)</option>
              <option value={3}>3 — Elevated / Well Above Normal (&ge; 240 mg/dL)</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Fasting Glucose Level</label>
            <select name="gluc" className="form-select" value={formData.gluc} onChange={onChange}>
              <option value={1}>1 — Normal Range (&lt; 100 mg/dL)</option>
              <option value={2}>2 — Impaired / Above Normal (100-125 mg/dL)</option>
              <option value={3}>3 — Elevated / Diabetic Range (&ge; 126 mg/dL)</option>
            </select>
          </div>
        </div>
      </div>

      {/* 5. Behavioral & Lifestyle */}
      <div className="form-section">
        <div className="form-section-header">
          <div className="form-section-icon"><HeartHandshake size={18} /></div>
          <h3 className="form-section-title">Behavioral Risk Factors</h3>
        </div>
        <div className="form-grid">
          <div className="form-group">
            <label className="form-label">Tobacco Smoking</label>
            <select name="smoke" className="form-select" value={formData.smoke} onChange={onChange}>
              <option value={0}>Non-Smoker</option>
              <option value={1}>Active Smoker</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Alcohol Intake</label>
            <select name="alco" className="form-select" value={formData.alco} onChange={onChange}>
              <option value={0}>None / Occasional</option>
              <option value={1}>Regular Alcohol Consumption</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Physical Activity</label>
            <select name="active" className="form-select" value={formData.active} onChange={onChange}>
              <option value={1}>Physically Active (&ge; 150 mins/week)</option>
              <option value={0}>Sedentary / Inactive</option>
            </select>
          </div>
        </div>
      </div>

      <button type="submit" className="btn-primary btn-full" disabled={loading}>
        {loading ? (
          <><span className="spinner" /> Running Ensemble Inference...</>
        ) : (
          <><Play size={18} /> Compute Cardiovascular Risk Stratification</>
        )}
      </button>
    </form>
  );
}
