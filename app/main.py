from fastapi import FastAPI
from schemas import TicketInput, TriageResult

app = FastAPI()

@app.get('/health')
async def health():
    return {'status': 'ok'}


@app.post('/triage')
async def triage_ticket(req: TicketInput) -> TriageResult:
    pass

@app.post('/batch-triage')
async def batch_triage_ticket(req: list[TicketInput]) -> list[TriageResult]:
    pass