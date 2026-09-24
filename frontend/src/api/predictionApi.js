const API_BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Send patient data to the Stacking Ensemble model.
 * Automatically tries relative proxy, 127.0.0.1, and localhost.
 * Returns { prediction: float, has_cardio_disease: bool, risk_level: string, bmi: float }
 */
export async function getPrediction(payload) {
  const endpoints = [
    API_BASE_URL ? `${API_BASE_URL}/predict` : '/predict',
    'http://127.0.0.1:8000/predict',
    'http://localhost:8000/predict'
  ].filter((v, i, a) => a.indexOf(v) === i && v);

  let lastError = null;

  for (const url of endpoints) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (response.status === 422) {
        const detail = await response.json();
        throw new Error(`Validation error: ${JSON.stringify(detail.detail)}`);
      }
      if (response.status === 500) {
        throw new Error('MODEL_ERROR');
      }
      if (!response.ok) {
        throw new Error('API_ERROR');
      }

      return await response.json();
    } catch (err) {
      lastError = err;
      if (err.message === 'MODEL_ERROR' || (err.message && err.message.startsWith('Validation error:'))) {
        throw err;
      }
      // Continue to try the next candidate endpoint
    }
  }

  throw lastError || new Error('Failed to fetch');
}
