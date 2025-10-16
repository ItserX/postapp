from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_post():
    payload = {"title": "Тестовый пост", "content": "Привет из теста!"}
    response = client.post("/posts", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["content"] == payload["content"]
    assert "id" in data


def test_get_posts():
    response = client.get("/posts")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "id" in data[0]
        assert "title" in data[0]
        assert "content" in data[0]
