import json
import pytest
from app import app as flask_app


@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(app, client):
    res = client.get('/spyt')
    assert res.status_code == 200
    j = json.loads(res.get_data(as_text=True))
    assert 10 == len(j)
    