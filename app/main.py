from fastapi import FastAPI

from app.schemas import TicketInput, TriageResult
from app.triage import triage_ticket

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/triage")
async def triage(req: TicketInput) -> TriageResult:
    return triage_ticket(req)


@app.post("/batch-triage")
async def batch_triage(req: list[TicketInput]) -> list[TriageResult]:
    return [triage_ticket(ticket) for ticket in req]

@app.get('/openapi')
async def openapi() -> dict:
    return app.openapi()