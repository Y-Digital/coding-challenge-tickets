# AI Text Triage API — Interview Assignment

## Goal

Build a small Python service that triages customer support tickets using an LLM
(Azure OpenAI).

**Timebox: 2 hours.** Stop at the time limit and write what you'd do next in
`NOTES.md`. Incomplete is perfectly OK — we value engineering judgment over
feature count.

---

## Endpoints

### `POST /triage`

Triage a single support ticket.

**Request:**

```json
{
  "subject": "Cannot access billing portal",
  "body": "I keep getting a 403 error when I try to open the billing page...",
  "customer_tier": "enterprise"
}
```

**Response:**

```json
{
  "category": "billing",
  "priority": "high",
  "summary": "Enterprise customer unable to access billing portal due to 403 error.",
  "actions": ["Escalate to billing team", "Check IAM permissions for customer org"],
  "confidence": 0.92
}
```

| Field        | Type                                                     |
| ------------ | -------------------------------------------------------- |
| `category`   | `billing \| bug \| feature_request \| security \| other` |
| `priority`   | `low \| medium \| high \| urgent`                        |
| `summary`    | One-sentence string                                      |
| `actions`    | List of recommended next-step strings                    |
| `confidence` | Float 0.0–1.0                                            |

### `POST /batch-triage`

Triage multiple tickets in one call.

**Request:** a JSON array of ticket objects (same shape as `/triage` input).

**Response:** a JSON array of triage results.

---

## What You Need to Do

The scaffold is a working FastAPI app. The only piece missing is the LLM call.

**Your main task:** implement the `triage_ticket()` function in `app/llm.py`.

This function should:

1. Call Azure OpenAI with a prompt that includes the ticket details
2. Instruct the model to return JSON matching the `TriageResult` schema
3. Parse and validate the response using Pydantic
4. If the model returns invalid JSON, retry once with a "fix it" prompt

Everything else (endpoints, schemas, tests, Docker) is already wired up and
will work once `triage_ticket()` is implemented.

### Must Have

- [ ] `triage_ticket()` calls Azure OpenAI and returns a valid `TriageResult`
- [ ] Handles invalid LLM output gracefully (retry / repair)
- [ ] All tests pass (`make test`)
- [ ] Runs locally (`make run` or `docker compose up`)
- [ ] No secrets committed to git

### Nice to Have

- [ ] Structured logging (JSON format)
- [ ] Retry with back-off on transient LLM errors
- [ ] Concurrency or rate limiting in `/batch-triage`
- [ ] Additional tests

---

## Project Structure

```
app/
  main.py       ← FastAPI app + endpoints (provided, no changes needed)
  schemas.py    ← Pydantic models for request/response (provided)
  llm.py        ← ★ YOUR TODO: implement triage_ticket()
tests/
  conftest.py   ← Test setup: mocks out the LLM call
  test_api_validation.py    ← Tests for input validation (422s)
  test_triage_mocked.py     ← Tests with mocked LLM (deterministic)
data/
  tickets.jsonl ← 25 sample tickets for manual testing
```

---

## Environment Variables

These will be provided to you. **Do not commit real values.**

| Variable                    | Description                              |
| --------------------------- | ---------------------------------------- |
| `AZURE_OPENAI_ENDPOINT`    | e.g. `https://<name>.openai.azure.com/`  |
| `AZURE_OPENAI_API_KEY`     | API key for the resource                 |
| `AZURE_OPENAI_DEPLOYMENT`  | Model deployment name                    |
| `AZURE_OPENAI_API_VERSION` | e.g. `2024-06-01`                        |

Copy `.env.example` to `.env` and fill in the values you receive.

---

## Running Locally

```bash
# With Docker
make build
make run          # or: docker compose up

# Without Docker
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your values
make dev               # or: uvicorn app.main:app --reload
```

## Running Tests

```bash
make test         # or: pytest -v
```

Tests use a mock — they don't need Azure credentials or network access.

---

## Evaluation Rubric (20 points)

| Area                   | Points | What we look for                                                        |
| ---------------------- | ------ | ----------------------------------------------------------------------- |
| **Python + API**       | 0–6    | Clean code, Pydantic use, error handling, sensible structure            |
| **AI Integration**     | 0–6    | Prompt quality, JSON schema enforcement, repair logic, mocked tests     |
| **DevOps + Packaging** | 0–6    | Env vars, no committed secrets, Docker works, project layout            |
| **Communication**      | 0–2    | README updates, NOTES.md with tradeoffs and next steps                  |

---

## How to Submit

1. Create a branch named `solution/<your-name>` and commit your work there.
2. Push the branch and let us know via email.
3. Include a completed `NOTES.md` (max 1 page): what works, what's missing,
   how you'd productionise.

Good luck!
