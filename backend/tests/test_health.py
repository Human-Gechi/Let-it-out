from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas import HealthResponse

client = TestClient(app)


@patch("backend.app.routers.health.check_ai_status")
def test_health_endpoint_ok(mock_check_ai_status):
    mock_check_ai_status.return_value = HealthResponse(
        status="ok",
        ai_enabled=True,
        ai_reachable=True,
        ai_reason=None,
    )

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["ai_enabled"] is True
    assert data["ai_reachable"] is True
    assert data["ai_reason"] is None


@patch("backend.app.routers.health.check_ai_status")
def test_health_endpoint_degraded(mock_check_ai_status):
    mock_check_ai_status.return_value = HealthResponse(
        status="degraded",
        ai_enabled=True,
        ai_reachable=False,
        ai_reason="AI API key is missing or empty",
    )

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["ai_enabled"] is True
    assert data["ai_reachable"] is False


@patch("backend.app.routers.health.check_ai_status")
def test_health_endpoint_disabled(mock_check_ai_status):
    mock_check_ai_status.return_value = HealthResponse(
        status="disabled",
        ai_enabled=False,
        ai_reachable=False,
        ai_reason="AI feature is disabled in settings",
    )

    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "disabled"
    assert data["ai_enabled"] is False
    assert data["ai_reachable"] is False
