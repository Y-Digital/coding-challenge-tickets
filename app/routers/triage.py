"""
Triage router — exposes /triage and /batch-triage endpoints.

TODO: Wire up the real LLM client and add request-id logging / timing.
"""

from __future__ import annotations

import logging
import time
import uuid

from fastapi import APIRouter, Request, Response

from app.schemas import TicketInput, TriageResult
from app.services.triage_service import triage_batch, triage_single

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/triage", response_model=TriageResult)
async def triage_endpoint(ticket: TicketInput, request: Request):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()

    logger.info("triage.start", extra={"request_id": request_id})

    # TODO: get `llm_client` from app state or dependency injection
    llm_client = request.app.state.llm_client
    result = await triage_single(llm_client, ticket)

    elapsed = time.perf_counter() - start
    logger.info(
        "triage.done",
        extra={"request_id": request_id, "elapsed_s": round(elapsed, 3)},
    )
    return result


@router.post("/batch-triage", response_model=list[TriageResult])
async def batch_triage_endpoint(tickets: list[TicketInput], request: Request):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()

    logger.info(
        "batch_triage.start",
        extra={"request_id": request_id, "ticket_count": len(tickets)},
    )

    llm_client = request.app.state.llm_client
    results = await triage_batch(llm_client, tickets)

    elapsed = time.perf_counter() - start
    logger.info(
        "batch_triage.done",
        extra={"request_id": request_id, "elapsed_s": round(elapsed, 3)},
    )
    return results
