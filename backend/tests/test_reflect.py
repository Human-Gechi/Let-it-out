from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Welcom to Let It Out API"
    assert "docs" and "health" in body


def test_reflect_for_normal_text_safe():

    payload = {
        "letter_text": "I wish my ex never left me. I really loved him so much",
        "recipient_type": "ex",
        "tone": "gentle",
    }

    response = client.post("/reflect", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["safe_to_release"] is True
    assert "reflection" in body
    assert body["resource_note"] is None


def test_reflect_for_normal_text_unsafe():

    payload = {
        "letter_text": "I hate myself and want to kill myself",
        "recipient_type": "ex",
        "tone": "gentle",
    }

    response = client.post("/reflect", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["safe_to_release"] is True
    assert "reflection" in body
    assert body["resource_note"] is None
