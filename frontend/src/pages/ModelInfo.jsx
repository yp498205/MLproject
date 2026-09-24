import React from 'react';
import { Cpu, CheckCircle2, Award, Zap, Layers, BarChart3 } from 'lucide-react';

export default function ModelInfo() {
  const models = [
    {
      name: 'Stacking Classifier Ensemble',
      type: 'Heterogeneous Meta-Ensemble',
      accuracy: '73.53%',
      testAcc: '73.20%',
      auc: '0.8048',
      f1: '0.7165',
      status: 'Active (Production)',
      highlight: true
    },
    {
      name: 'HistGradientBoosting',
      type: 'Binned Gradient Boosting',
      accuracy: '73.56%',
      testAcc: '73.15%',
      auc: '0.7999',
      f1: '0.7151',
      status: 'Base Learner',
      highlight: false
    },
    {
      name: 'XGBoost (Extreme Gradient Boost)',
      type: 'Regularized Tree Ensemble',
      accuracy: '73.50%',
      testAcc: '73.08%',
      auc: '0.7991',
      f1: '0.7145',
      status: 'Base Learner',
      highlight: false
    },
    {
      name: 'LightGBM (Light Gradient Boost)',
      type: 'Leaf-wise Tree Ensemble',
      accuracy: '73.50%',
      testAcc: '73.09%',
      auc: '0.7991',
      f1: '0.7147',
      status: 'Base Learner',
      highlight: false
    },
    {
      name: 'Decision Tree Classifier',
      type: 'Single Decision Tree (depth=5)',
      accuracy: '73.11%',
      testAcc: '73.11%',
      auc: '0.7919',
      f1: '0.7134',
      status: 'Baseline Evaluated',
      highlight: false
    },
    {
      name: 'Logistic Regression (Sklearn)',
      type: 'L2 Regularized Generalized Linear',
      accuracy: '72.75%',
      testAcc: '72.67%',
      auc: '0.7935',
      f1: '0.7070',
      status: 'Meta Learner',
      highlight: false
    },
    {
      name: 'Logistic Regression (Scratch)',
      type: 'Custom Gradient Descent Algorithm',
      accuracy: '72.70%',
      testAcc: '72.70%',
      auc: '0.7920',
      f1: '0.7065',
      status: 'Algorithm Validation',
      highlight: false
    }
  ];

  const topFeatures = [
    { name: 'Systolic Blood Pressure (ap_hi)', weight: '38.4%', desc: 'Primary cardiovascular indicator' },
    { name: 'Age in Years', weight: '22.1%', desc: 'Cumulative vascular exposure risk' },
    { name: 'Serum Cholesterol Tier', weight: '14.8%', desc: 'Atherosclerotic plaque accumulation' },
    { name: 'Body Mass Index (BMI)', weight: '10.2%', desc: 'Adiposity and metabolic load' },
    { name: 'Mean Arterial Pressure (MAP)', weight: '7.5%', desc: 'Calculated continuous perfusion metric' },
    { name: 'Glucose Level & Lifestyle', weight: '7.0%', desc: 'Glycemic control and physical habits' }
  ];

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            <Cpu color="var(--color-primary)" />
            Model Benchmarks & Empirical Evaluation
          </h2>
          <p className="card-subtitle">
            Rigorous cross-validation conducted over 68,640 filtered records from the cardiovascular disease clinical dataset.
          </p>
        </div>

        {/* Benchmarks Table */}
        <div className="data-table-container">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Model Architecture</th>
                <th>Classification Paradigm</th>
                <th>CV Accuracy</th>
                <th>Test Accuracy</th>
                <th>Test ROC-AUC</th>
                <th>F1 Score</th>
                <th>Pipeline Role</th>
              </tr>
            </thead>
            <tbody>
              {models.map((m, idx) => (
                <tr key={idx} className={m.highlight ? 'highlight-row' : ''}>
                  <td style={{ fontWeight: '700' }}>
                    {m.highlight && (
                      <CheckCircle2 size={15} color="var(--color-success)" style={{ display: 'inline', marginRight: '6px', verticalAlign: 'middle' }} />
                    )}
                    {m.name}
                  </td>
                  <td>{m.type}</td>
                  <td style={{ fontWeight: '700', color: 'var(--color-primary)' }}>{m.accuracy}</td>
                  <td>{m.testAcc}</td>
                  <td style={{ fontWeight: '700', color: 'var(--color-accent)' }}>{m.auc}</td>
                  <td>{m.f1}</td>
                  <td>
                    <span className={`badge-tag ${m.highlight ? 'active' : 'baseline'}`}>
                      {m.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="insight-box">
          <div className="insight-title">Ensemble Validation Strategy</div>
          <p className="insight-text">
            Models were compared using <strong>Repeated Stratified K-Fold Cross-Validation</strong> (3 splits, 2 repeats). The meta-classifier combines predictions from tree-based boosting algorithms with a regularized logistic meta-layer to minimize residual variance and maximize generalizability.
          </p>
        </div>
      </div>

      {/* Feature Importance Card */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">
            <BarChart3 color="var(--color-accent)" />
            Feature Importance & Clinical Significance
          </h2>
          <p className="card-subtitle">
            Relative predictive weight of input parameters and derived engineered features across the ensemble.
          </p>
        </div>

        <div className="arch-grid">
          {topFeatures.map((feat, idx) => (
            <div key={idx} className="arch-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                <h3 style={{ margin: 0 }}>{feat.name}</h3>
                <span style={{ fontWeight: '700', color: 'var(--color-primary)', fontSize: '0.95rem' }}>{feat.weight}</span>
              </div>
              <p>{feat.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
