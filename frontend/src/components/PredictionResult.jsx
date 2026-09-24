import React from 'react';
import { AlertTriangle, CheckCircle, ShieldAlert, Activity, Heart, Info, Check, ShieldCheck } from 'lucide-react';

function getInterpretation(probability) {
  if (probability < 0.30) {
    return {
      level: 'low',
      badge: 'Low Cardiovascular Risk',
      description: 'Patient biometric profile falls within normal statistical thresholds. Continue balanced nutrition and regular physical activity.',
      statusClass: 'status-low',
      riskClass: 'risk-low',
      fillClass: 'fill-low',
      textClass: 'text-success'
    };
  }
  if (probability < 0.50) {
    return {
      level: 'moderate',
      badge: 'Borderline / Moderate Risk',
      description: 'Key biomarkers indicate mild risk elevation. Preventive dietary adjustments and lifestyle interventions are suggested.',
      statusClass: 'status-moderate',
      riskClass: 'risk-moderate',
      fillClass: 'fill-moderate',
      textClass: 'text-warning'
    };
  }
  return {
    level: 'high',
    badge: 'Elevated Cardiovascular Risk',
    description: 'Clinical markers show elevated probability for cardiovascular disease. Recommend comprehensive medical evaluation and risk factor management.',
    statusClass: 'status-high',
    riskClass: 'risk-high',
    fillClass: 'fill-high',
    textClass: 'text-danger'
  };
}

export default function PredictionResult({ result, formData }) {
  const probability = result.prediction;
  const hasDisease = result.has_cardio_disease;
  const probabilityPct = (probability * 100).toFixed(1);
  
  const bmi = result.bmi || (formData.weight / Math.pow(formData.height / 100, 2)).toFixed(1);
  const pulsePressure = formData.ap_hi - formData.ap_lo;
  const meanArterialPressure = (formData.ap_lo + (pulsePressure / 3)).toFixed(1);
  
  const interp = getInterpretation(probability);

  return (
    <div className={`result-card ${interp.riskClass}`}>
      <div className="result-header">
        <div>
          <h3 className="card-title">
            <Activity size={20} color="var(--color-primary)" />
            Risk Stratification Analysis
          </h3>
          <p className="card-subtitle" style={{ margin: 0 }}>
            Model Output: Stacking Classifier Ensemble
          </p>
        </div>
        
        <div className={`result-badge-pill ${interp.statusClass}`}>
          {hasDisease ? (
            <><AlertTriangle size={16} /> {interp.badge}</>
          ) : (
            <><ShieldCheck size={16} /> {interp.badge}</>
          )}
        </div>
      </div>

      {/* Visual Probability Gauge */}
      <div className="gauge-container">
        <div className="gauge-header">
          <div className="gauge-title">
            <Heart size={18} />
            Calculated Risk Probability
          </div>
          <div className={`gauge-value ${interp.textClass}`}>
            {probabilityPct}%
          </div>
        </div>
        
        <div className="gauge-track">
          <div 
            className={`gauge-fill ${interp.fillClass}`} 
            style={{ width: `${Math.max(6, Math.min(100, probability * 100))}%` }}
          />
        </div>
        <div className="gauge-markers">
          <span>0% (Optimal)</span>
          <span>30% (Borderline)</span>
          <span>50% (Clinical Threshold)</span>
          <span>100% (High)</span>
        </div>
      </div>

      {/* Computed Hemodynamic & Clinical Metrics */}
      <div className="clinical-grid">
        <div className="clinical-box">
          <span className="clinical-label">Body Mass Index</span>
          <div className="clinical-val">{bmi} kg/m²</div>
          <div className="clinical-desc">
            {bmi < 25 ? 'Normal BMI' : bmi < 30 ? 'Overweight' : 'Obese'}
          </div>
        </div>

        <div className="clinical-box">
          <span className="clinical-label">Blood Pressure</span>
          <div className="clinical-val">{formData.ap_hi} / {formData.ap_lo}</div>
          <div className="clinical-desc">
            {formData.ap_hi < 120 && formData.ap_lo < 80 ? 'Normal Blood Pressure' : 'Elevated / Hypertensive'}
          </div>
        </div>

        <div className="clinical-box">
          <span className="clinical-label">Pulse Pressure</span>
          <div className="clinical-val">{pulsePressure} mmHg</div>
          <div className="clinical-desc">
            {pulsePressure <= 40 ? 'Normal stiffness' : 'Elevated arterial stiffness'}
          </div>
        </div>

        <div className="clinical-box">
          <span className="clinical-label">Mean Arterial (MAP)</span>
          <div className="clinical-val">{meanArterialPressure} mmHg</div>
          <div className="clinical-desc">Perfusion pressure index</div>
        </div>
      </div>

      {/* Narrative Clinical Insight */}
      <div className="insight-box">
        <div className="insight-title">Clinical Interpretation</div>
        <p className="insight-text">{interp.description}</p>
      </div>
    </div>
  );
}
