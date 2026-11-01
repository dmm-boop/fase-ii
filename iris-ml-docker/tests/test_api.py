from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
VALID = {'sepal_length':5.1,'sepal_width':3.5,'petal_length':1.4,'petal_width':0.2}

def test_home():
    r = client.get('/')
    assert r.status_code == 200 and 'Clasificador' in r.text

def test_health():
    assert client.get('/api/health').json()['status'] == 'ok'

def test_predict():
    r = client.post('/api/predict', json=VALID)
    assert r.status_code == 200
    data = r.json()
    assert data['species'] == 'setosa'
    assert abs(sum(data['probabilities'].values()) - 1) < 0.001

def test_missing_field():
    assert client.post('/api/predict', json={'sepal_length':5}).status_code == 422

def test_negative_value():
    assert client.post('/api/predict', json={**VALID,'petal_width':-1}).status_code == 422

def test_out_of_range():
    assert client.post('/api/predict', json={**VALID,'petal_width':21}).status_code == 422

def test_invalid_type():
    assert client.post('/api/predict', json={**VALID,'petal_width':'texto'}).status_code == 422

def test_boundary_zero():
    assert client.post('/api/predict', json={**VALID,'petal_width':0}).status_code == 200

def test_openapi():
    assert '/api/predict' in client.get('/openapi.json').json()['paths']
