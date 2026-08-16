from backend.app.services import ai_client


def test_prompt_response_matches_frontend_contract(api_request):
    response = api_request("GET", "/prompt", params={"recipient_type": "other"})

    assert response.status_code == 200
    assert response.json().keys() == {"prompt", "recipient_type"}
    assert response.json()["recipient_type"] == "other"


def test_reflection_falls_back_when_ai_is_disabled(api_request, monkeypatch):
    monkeypatch.setattr(ai_client.settings, "AI_ENABLED", False)
    response = api_request(
        "POST",
        "/reflect",
        json={
            "letter_text": "I needed to say this somewhere.",
            "recipient_type": "other",
            "tone": "gentle",
        },
    )

    assert response.status_code == 200
    assert response.json()["safe_to_release"] is True
    assert response.json()["resource_note"] is None
    assert response.json()["reflection"]


def test_flagged_reflection_returns_crisis_resource(api_request):
    response = api_request(
        "POST",
        "/reflect",
        json={
            "letter_text": "I want to die.",
            "recipient_type": "other",
            "tone": "gentle",
        },
    )

    assert response.status_code == 200
    assert response.json()["safe_to_release"] is False
    assert response.json()["resource_note"]
