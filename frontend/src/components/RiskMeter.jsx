import React from 'react';
import { Activity } from 'lucide-react';

export default function RiskMeter({ probability, level, hasDisease }) {
  const percentage = (probability * 100).toFixed(1);

  return (
    <div className="gauge-container">
      <div className="gauge-header">
        <div className="gauge-title">
          <Activity size={18} />
          Model Predicted Probability
        </div>
        <div className={`gauge-value ${hasDisease ? 'text-danger' : 'text-success'}`}>
          {percentage}%
        </div>
      </div>
      
      <div className="gauge-track">
        <div 
          className={`gauge-fill fill-${level}`} 
          style={{ width: `${Math.max(5, Math.min(100, probability * 100))}%` }}
        />
      </div>
      <div className="gauge-markers">
        <span>0% (Low)</span>
        <span>50% (Threshold)</span>
        <span>100% (High)</span>
      </div>
    </div>
  );
}
