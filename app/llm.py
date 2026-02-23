"""
LLM integration — call Azure OpenAI and return a validated TriageResult.

TODO (candidate): Implement the `triage_ticket` function.

Hints:
    - Use the `openai` Python SDK with `openai.AzureOpenAI(...)`.
    - Build a system prompt that includes the expected JSON schema.
    - Parse the response with `TriageResult.model_validate_json(...)`.
    - If parsing fails, retry once with a "fix the JSON" follow-up prompt.
"""

import os

from app.schemas import TicketInput, TriageResult


def triage_ticket(ticket: TicketInput) -> TriageResult:
    """Call Azure OpenAI to triage a single support ticket.

    Environment variables you can use:
        AZURE_OPENAI_ENDPOINT
        AZURE_OPENAI_API_KEY
        AZURE_OPENAI_DEPLOYMENT
        AZURE_OPENAI_API_VERSION
    """
    raise NotImplementedError("Implement Azure OpenAI integration here")
