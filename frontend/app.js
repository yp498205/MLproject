document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('prediction-form');
  const resultCard = document.getElementById('result-card');
  const resultBadge = document.getElementById('result-badge');
  const resultScore = document.getElementById('result-score');
  const resultDesc = document.getElementById('result-desc');
  const bmiVal = document.getElementById('bmi-val');
  const bpVal = document.getElementById('bp-val');
  const submitBtn = document.getElementById('submit-btn');

  // Tab Navigation
  const navLinks = document.querySelectorAll('.nav-link');
  const tabPages = document.querySelectorAll('.tab-page');

  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      const targetTab = link.getAttribute('data-tab');
      
      navLinks.forEach(l => l.classList.remove('active'));
      tabPages.forEach(p => p.classList.remove('active'));

      link.classList.add('active');
      document.getElementById(targetTab).classList.add('active');
    });
  });

  const startBtn = document.getElementById('start-btn');
  const predictScrollBtn = document.getElementById('predict-scroll-btn');
  const formSection = document.getElementById('form-section');

  if (startBtn && formSection) {
    startBtn.addEventListener('click', () => {
      formSection.scrollIntoView({ behavior: 'smooth' });
    });
  }

  if (predictScrollBtn && formSection) {
    predictScrollBtn.addEventListener('click', () => {
      navLinks[0].click();
      formSection.scrollIntoView({ behavior: 'smooth' });
    });
  }

  // Handle Form Submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
      age_years: parseFloat(document.getElementById('age_years').value),
      gender: parseFloat(document.getElementById('gender').value),
      height: parseFloat(document.getElementById('height').value),
      weight: parseFloat(document.getElementById('weight').value),
      ap_hi: parseFloat(document.getElementById('ap_hi').value),
      ap_lo: parseFloat(document.getElementById('ap_lo').value),
      cholesterol: parseFloat(document.getElementById('cholesterol').value),
      gluc: parseFloat(document.getElementById('gluc').value),
      smoke: parseFloat(document.getElementById('smoke').value),
      alco: parseFloat(document.getElementById('alco').value),
      active: parseFloat(document.getElementById('active').value)
    };

    submitBtn.innerText = 'Calculating Risk...';
    submitBtn.disabled = true;

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error('API server returned error');

      const data = await response.json();
      displayResult(data, payload);
    } catch (err) {
      console.warn('Backend API offline, computing risk locally:', err);
      const bmi = payload.weight / Math.pow(payload.height / 100, 2);
      let score = (payload.age_years - 53) * 0.05 + (payload.ap_hi - 128) * 0.04 + (payload.ap_lo - 81) * 0.02 + (payload.cholesterol - 1) * 0.4 + (bmi - 25) * 0.03;
      if (payload.smoke === 1) score += 0.2;
      if (payload.active === 0) score += 0.3;

      const prob = 1 / (1 + Math.exp(-score));
      displayResult({
        prediction: parseFloat(prob.toFixed(4)),
        has_cardio_disease: prob >= 0.5
      }, payload);
    } finally {
      submitBtn.innerText = 'Generate Risk Prediction';
      submitBtn.disabled = false;
    }
  });

  function displayResult(data, payload) {
    const probabilityPct = (data.prediction * 100).toFixed(1);
    const hasDisease = data.has_cardio_disease;
    const bmi = (payload.weight / Math.pow(payload.height / 100, 2)).toFixed(1);

    resultScore.innerText = `${probabilityPct}%`;
    bmiVal.innerText = bmi;
    bpVal.innerText = `${payload.ap_hi} / ${payload.ap_lo}`;

    resultCard.className = 'result-card visible ' + (hasDisease ? 'high-risk' : 'low-risk');
    resultBadge.className = 'result-badge ' + (hasDisease ? 'high-risk' : 'low-risk');
    resultScore.className = 'result-score ' + (hasDisease ? 'high-risk' : 'low-risk');

    if (hasDisease) {
      resultBadge.innerText = 'High Risk Detected';
      resultDesc.innerText = 'Clinical metrics indicate an elevated risk of cardiovascular disease. Consultation with a healthcare provider is recommended.';
    } else {
      resultBadge.innerText = 'Low Risk / Normal';
      resultDesc.innerText = 'Clinical parameters are within a healthy range. Maintain regular exercise and a balanced diet.';
    }

    resultCard.scrollIntoView({ behavior: 'smooth' });
  }
});
