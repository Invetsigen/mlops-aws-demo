from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_predict():
    body = {"mean_radius": 12.0, "mean_texture": 18.0, "mean_smoothness": 0.09,
            "mean_compactness": 0.08, "mean_symmetry": 0.17}
    r = client.post("/predict", json=body)
    assert r.status_code == 200
    assert 0 <= r.json()["benign_probability"] <= 1
