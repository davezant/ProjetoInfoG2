import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Adjust this import to your main application entrypoint
# For example, if your app is in app/main.py and called "app":
# from app.main import app

# For demonstration, we'll construct a minimal FastAPI app here.
# Replace this with your actual app import.
def get_app():
    app = FastAPI()

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    @app.get("/items/{item_id}")
    def get_item(item_id: int, q: str = None):
        return {"item_id": item_id, "q": q}

    @app.post("/items/")
    def create_item(item: dict):
        return {"created": item}

    return app

@pytest.fixture
def client():
    app = get_app()
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_item(client):
    response = client.get("/items/42?q=foo")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "q": "foo"}

def test_create_item(client):
    data = {"name": "Test Item", "price": 10.5}
    response = client.post("/items/", json=data)
    assert response.status_code == 200
    assert response.json() == {"created": data}

def test_not_found(client):
    response = client.get("/nonexistent/endpoint")
    assert response.status_code == 404
