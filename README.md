# AI Text Triage API — Interview Assignment

## Goal

Build and deploy a small Python service that ingests support tickets and returns
structured triage information using an LLM (Azure OpenAI).

**Timebox: 2 hours.** Stop at the time limit and write what you'd do next in `NOTES.md`.
Incomplete is perfectly OK — we value engineering judgment over feature count.

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

| Field        | Type                                                  |
| ------------ | ----------------------------------------------------- |
| `category`   | `billing \| bug \| feature_request \| security \| other` |
| `priority`   | `low \| medium \| high \| urgent`                       |
| `summary`    | One-sentence string                                   |
| `actions`    | List of recommended next-step strings                 |
| `confidence` | Float 0.0–1.0                                         |

### `POST /batch-triage`

Triage multiple tickets in one call.

**Request:** a JSON array of ticket objects (same shape as `/triage` input).

**Response:** a JSON array of triage results.

**Requirements:**
- Process tickets concurrently (async or thread pool).
- Apply basic rate limiting so you don't hammer the LLM API.

---

## Must Have

- [ ] FastAPI service with `/triage` and `/batch-triage`
- [ ] Uses Azure OpenAI (env vars provided) to produce the JSON output
- [ ] Validates LLM output with Pydantic; handles invalid JSON gracefully (retry / repair)
- [ ] At least **two tests** with the LLM call mocked:
  1. API input validation test
  2. Deterministic triage result test (mocked LLM)
- [ ] Dockerfile and instructions to run locally (`make run` or `docker compose up`)
- [ ] Request-level logging: request id, timing, errors

## Nice to Have

- [ ] Deployed to Azure Container Apps
- [ ] Structured logging (JSON)
- [ ] Retry policy with back-off on LLM calls
- [ ] Simple rate limiter for `/batch-triage`

---

## Environment Variables

These will be provided to you. **Do not commit real values.**

| Variable                     | Description                          |
| ---------------------------- | ------------------------------------ |
| `AZURE_OPENAI_ENDPOINT`     | e.g. `https://<name>.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY`      | API key for the resource             |
| `AZURE_OPENAI_DEPLOYMENT`   | Model deployment name                |
| `AZURE_OPENAI_API_VERSION`  | e.g. `2024-06-01`                    |

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

---

## Deploying to Azure Container Apps

See `deploy/deploy.sh` for a template script. Fill in the resource names you
receive and run it.

---

## Evaluation Rubric (20 points)

| Area                    | Points | What we look for                                                    |
| ----------------------- | ------ | ------------------------------------------------------------------- |
| **Python + API**        | 0–6    | Clean FastAPI, Pydantic models, sensible structure, async, errors   |
| **AI Integration**      | 0–6    | Prompt discipline, schema enforcement, JSON repair, mocked tests    |
| **Azure + Deployment**  | 0–6    | Env vars, no committed secrets, deploys or clear explanation of gap |
| **Communication**       | 0–2    | README updates, NOTES.md with tradeoffs and next steps              |

---

## Deliverables

1. Repo link or zip
2. `NOTES.md` (max 1 page): what works, what's missing, how you'd productionise

Good luck!
