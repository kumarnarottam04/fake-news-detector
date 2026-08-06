import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'model_loaded' in data

def test_samples_endpoint(client):
    response = client.get('/api/samples')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'samples' in data

def test_predict_endpoint_valid_real(client):
    payload = {
        "text": "Official Government Bureau releases quarterly employment and economic growth metrics showing steady market stabilization across domestic sectors."
    }
    response = client.post(
        '/api/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'prediction' in data
    assert data['prediction']['label'] in ['REAL', 'FAKE']
    assert 'confidence' in data['prediction']

def test_predict_endpoint_short_text_validation(client):
    payload = {"text": "Too short news"}
    response = client.post(
        '/api/predict',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False
    assert data['error']['code'] == 'INVALID_INPUT'
