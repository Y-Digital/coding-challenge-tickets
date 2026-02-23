"""
Triage service — orchestrates LLM calls for single and batch triage.

TODO: Implement batch processing with concurrency + rate limiting.
"""

from __future__ import annotations

import asyncio

from app.config import settings
from app.schemas import TicketInput, TriageResult
from app.services.llm_client import BaseLLMClient


async def triage_single(client: BaseLLMClient, ticket: TicketInput) -> TriageResult:
    """Triage one ticket via the LLM client."""
    return await client.triage_ticket(ticket)


async def triage_batch(
    client: BaseLLMClient, tickets: list[TicketInput]
) -> list[TriageResult]:
    """Triage a batch of tickets concurrently, respecting a concurrency limit.

    TODO:
        - Use an asyncio.Semaphore (or similar) to cap concurrency to
          `settings.llm_max_concurrency`.
        - Return results in the same order as the input list.
    """
    semaphore = asyncio.Semaphore(settings.llm_max_concurrency)

    async def _limited(ticket: TicketInput) -> TriageResult:
        async with semaphore:
            return await triage_single(client, ticket)

    return list(await asyncio.gather(*[_limited(t) for t in tickets]))
