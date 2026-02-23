"""
LLM client abstraction.

TODO: Implement the `triage_ticket` method.
      - Call Azure OpenAI Chat Completions.
      - Return ONLY valid JSON matching the TriageResult schema.
      - If parsing fails, retry once with a "fix the JSON" prompt.
"""

from __future__ import annotations

import abc

from app.schemas import TicketInput, TriageResult


class BaseLLMClient(abc.ABC):
    """Interface that both the real and mock clients implement."""

    @abc.abstractmethod
    async def triage_ticket(self, ticket: TicketInput) -> TriageResult:
        """Send a ticket to the LLM and return a validated TriageResult."""
        ...


class AzureOpenAIClient(BaseLLMClient):
    """Real client that talks to Azure OpenAI.

    TODO: implement this class.
    Hints:
        - Use `httpx.AsyncClient` or the `openai` Python SDK.
        - Build a system prompt that includes the JSON schema.
        - Parse the response with `TriageResult.model_validate_json(...)`.
        - On parse failure, send a follow-up "fix" prompt and retry once.
    """

    def __init__(self, endpoint: str, api_key: str, deployment: str, api_version: str):
        self.endpoint = endpoint
        self.api_key = api_key
        self.deployment = deployment
        self.api_version = api_version

    async def triage_ticket(self, ticket: TicketInput) -> TriageResult:
        raise NotImplementedError("Implement Azure OpenAI integration here")
