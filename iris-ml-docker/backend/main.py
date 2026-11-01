from functools import lru_cache
from pathlib import Path
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / 'backend' / 'modelo.joblib'
LABELS = ['setosa', 'versicolor', 'virginica']

class IrisInput(BaseModel):
    sepal_length: float = Field(..., ge=0, le=20, allow_inf_nan=False)
    sepal_width: float = Field(..., ge=0, le=20, allow_inf_nan=False)
    petal_length: float = Field(..., ge=0, le=20, allow_inf_nan=False)
    petal_width: float = Field(..., ge=0, le=20, allow_inf_nan=False)

@lru_cache
def get_model():
    return joblib.load(MODEL_PATH)  # Only load trusted, project-generated artifacts.

app = FastAPI(title='Clasificador Iris', version='1.0.0')

@app.get('/api/health')
def health():
    try:
        get_model()
        return {'status': 'ok', 'model': 'loaded'}
    except Exception:
        raise HTTPException(status_code=503, detail='Modelo no disponible')

@app.post('/api/predict')
def predict(data: IrisInput):
    model = get_model()
    features = [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]]
    prediction = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0]
    return {'species': LABELS[prediction], 'confidence': round(float(probabilities[prediction]), 4), 'probabilities': {name: round(float(p), 4) for name, p in zip(LABELS, probabilities)}}

app.mount('/static', StaticFiles(directory=ROOT / 'frontend'), name='static')

@app.get('/', include_in_schema=False)
def index():
    return FileResponse(ROOT / 'frontend' / 'index.html')
