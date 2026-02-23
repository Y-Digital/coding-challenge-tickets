"""
AI Text Triage API — FastAPI application.

TODO (candidate): implement `triage_ticket` in app/llm.py to make the
endpoints work end-to-end.
"""

import logging
import time
import uuid

from fastapi import FastAPI

from app.schemas import TicketInput, TriageResult
from app.llm import triage_ticket

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Text Triage API",
    version="0.1.0",
    description="Triage support tickets using an LLM.",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/triage", response_model=TriageResult)
def triage_endpoint(ticket: TicketInput):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    logger.info("triage.start request_id=%s", request_id)

    result = triage_ticket(ticket)

    elapsed = round(time.perf_counter() - start, 3)
    logger.info("triage.done request_id=%s elapsed_s=%s", request_id, elapsed)
    return result


@app.post("/batch-triage", response_model=list[TriageResult])
def batch_triage_endpoint(tickets: list[TicketInput]):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    logger.info("batch_triage.start request_id=%s count=%d", request_id, len(tickets))

    results = [triage_ticket(ticket) for ticket in tickets]

    elapsed = round(time.perf_counter() - start, 3)
    logger.info("batch_triage.done request_id=%s elapsed_s=%s", request_id, elapsed)
    return results
