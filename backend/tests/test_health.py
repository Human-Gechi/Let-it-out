from backend.app.services import ai_client


def test_health_reports_disabled_local_mode(api_request, monkeypatch):
    monkeypatch.setattr(ai_client.settings, "AI_ENABLED", False)
    response = api_request("GET", "/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "disabled",
        "ai_enabled": False,
        "ai_reachable": False,
        "ai_reason": "AI feature is disabled in settings",
    }
