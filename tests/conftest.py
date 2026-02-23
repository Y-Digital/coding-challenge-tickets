import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import TicketInput, TriageResult
from app.services.llm_client import BaseLLMClient


class MockLLMClient(BaseLLMClient):
    """Deterministic mock that always returns a fixed triage result."""

    async def triage_ticket(self, ticket: TicketInput) -> TriageResult:
        return TriageResult(
            category="bug",
            priority="high",
            summary=f"Mock triage for: {ticket.subject}",
            actions=["Investigate issue", "Notify engineering"],
            confidence=0.95,
        )


@pytest.fixture()
def mock_llm_client():
    return MockLLMClient()


@pytest.fixture()
def client(mock_llm_client):
    app.state.llm_client = mock_llm_client
    return TestClient(app)
