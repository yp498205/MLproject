const DEFAULT_CLOUD_API = 'https://cardioguard-backend-xzik.onrender.com';
const RAW_API_URL = import.meta.env.VITE_API_URL || DEFAULT_CLOUD_API;
const API_BASE_URL = RAW_API_URL.replace(/\/+$/, '');

/**
 * Send patient data to the Stacking Ensemble model.
 * Automatically attempts:
 * 1. Configured VITE_API_URL (Render backend)
 * 2. Relative proxy endpoint (/predict)
 * 3. Localhost endpoints (127.0.0.1:8000, localhost:8000)
 * 4. Fallback live Render backend
 * 
 * Returns { prediction: float, has_cardio_disease: bool, risk_level: string, bmi: float }
 */
export async function getPrediction(payload) {
  const endpoints = [
    `${API_BASE_URL}/predict`,
    '/predict',
    'http://127.0.0.1:8000/predict',
    'http://localhost:8000/predict',
    `${DEFAULT_CLOUD_API}/predict`
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
      // Try next endpoint in list
    }
  }

  throw lastError || new Error('Unable to connect to the prediction service.');
}
