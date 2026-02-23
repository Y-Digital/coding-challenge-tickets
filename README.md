# AI Text Triage API — Interview Assignment

## Goal

Build a Python service that triages customer support tickets using an LLM
(Azure OpenAI), containerise it, and prepare it for deployment to Kubernetes.

**Timebox: 2 hours.** Stop at the time limit and write what you'd do next in
`NOTES.md`. Incomplete is perfectly OK — we value engineering judgment over
feature count.

---

## What You're Given

```
app/
  __init__.py
  schemas.py       ← Pydantic models for request & response (do not change)
tests/
  conftest.py      ← Test fixtures — shows the expected app structure
  test_api_validation.py
  test_triage_mocked.py
data/
  tickets.jsonl    ← 25 sample tickets for manual testing
requirements.txt   ← Base dependencies (add more as needed)
Makefile           ← Expected commands: make dev, make test, make build, make run
.env.example       ← Azure OpenAI credentials template
```

## What You Need to Build

### 1. FastAPI application (`app/main.py`)

Create the FastAPI app with these endpoints:

#### `GET /health`

Returns `{"status": "ok"}`.

#### `POST /triage`

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

#### `POST /batch-triage`

Triage multiple tickets in one call.

**Request:** a JSON array of ticket objects (same shape as `/triage`).

**Response:** a JSON array of triage results.

### 2. LLM integration

Call Azure OpenAI to produce the triage output. Your implementation should:

- Build a prompt that instructs the model to return JSON matching the schema
- Parse and validate the response with Pydantic
- Handle invalid JSON from the model gracefully (retry or repair)

### 3. Dockerfile

Create a `Dockerfile` that builds and runs the service. The following should
work:

```bash
make build        # builds the Docker image
make run          # runs the container on port 8000
```

### 4. Kubernetes manifests

Create a `k8s/` directory with manifests to deploy the service to a Kubernetes
cluster. At minimum:

- `deployment.yaml` — runs the container, injects config via env vars or secrets
- `service.yaml` — exposes the service within the cluster

Use Kubernetes Secrets or ConfigMaps for the Azure OpenAI credentials — do not
hardcode them in the manifests.

---

## Tests

The test suite is provided. **All 5 tests should pass** once your app is
implemented. The tests mock the LLM call, so they need no Azure credentials.

```bash
make test         # or: pytest -v
```

> **Hint:** look at `tests/conftest.py` to understand the expected structure of
> your application — it shows how the mock is wired up.

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

## Must Have

- [ ] FastAPI app with `/health`, `/triage`, and `/batch-triage`
- [ ] Calls Azure OpenAI and returns valid `TriageResult` JSON
- [ ] Handles invalid LLM output (retry / repair)
- [ ] All provided tests pass
- [ ] `Dockerfile` — image builds and runs
- [ ] `k8s/` manifests — deployment + service, secrets not hardcoded
- [ ] No secrets committed to git

## Nice to Have

- [ ] Request logging (request id, timing)
- [ ] Retry with back-off on transient LLM errors
- [ ] Concurrency or rate limiting in `/batch-triage`
- [ ] Additional tests
- [ ] `docker-compose.yml` for local development

---

## Evaluation Rubric (20 points)

| Area                       | Points | What we look for                                                    |
| -------------------------- | ------ | ------------------------------------------------------------------- |
| **Python + API**           | 0–6    | Clean code, Pydantic use, error handling, working endpoints         |
| **AI Integration**         | 0–6    | Prompt quality, JSON schema enforcement, repair logic, tests pass   |
| **Docker + Kubernetes**    | 0–6    | Working Dockerfile, valid K8s manifests, secrets handling           |
| **Communication**          | 0–2    | NOTES.md with tradeoffs and next steps                              |

---

## How to Submit

1. Create a branch named `solution/<your-name>` and commit your work there.
2. Push the branch and let us know via email.
3. Include a completed `NOTES.md` (max 1 page): what works, what's missing,
   how you'd productionise.

Good luck!
