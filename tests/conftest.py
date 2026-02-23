import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.schemas import TriageResult


MOCK_RESULT = TriageResult(
    category="bug",
    priority="high",
    summary="Mock triage result",
    actions=["Investigate issue", "Notify engineering"],
    confidence=0.95,
)


@pytest.fixture()
def client():
    """Test client with the LLM call mocked out (no network, no API key needed)."""
    with patch("app.main.triage_ticket", return_value=MOCK_RESULT):
        from app.main import app

        yield TestClient(app)
