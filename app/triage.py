import os
from json import JSONDecodeError

import openai
from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import ValidationError

from app.schemas import TicketInput, TriageResult

load_dotenv()

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = openai.AzureOpenAI(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version=os.getenv('AZURE_OPENAI_API_VERSION'),
)

SYSTEM_PROMPT = """\
You are a support ticket classifier. Analyze the support ticket and respond with ONLY valid JSON.

Allowed values:
- category: billing | bug | feature_request | security | other
- priority: low | medium | high | urgent
- confidence: float between 0.0 and 1.0
- actions: list of strings (recommended next steps)
- summary: one sentence describing the issue

Customer tier influences priority: enterprise > business > free (higher tier = higher priority).

JSON schema (output ONLY this, no other text):
{
  "category": "<billing|bug|feature_request|security|other>",
  "priority": "<low|medium|high|urgent>",
  "summary": "<one sentence>",
  "actions": ["<action 1>", "<action 2>"],
  "confidence": <0.0 to 1.0>
}"""


def triage_ticket(ticket: TicketInput) -> TriageResult:
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {
            'role': 'user',
            'content': (
                f'Subject: {ticket.subject}\n'
                f'Body: {ticket.body}\n'
                f'Customer tier: {ticket.customer_tier.value}'
            ),
        },
    ]
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=messages,
            response_format={'type': 'json_object'},
        )
        content = response.choices[0].message.content
        return TriageResult.model_validate_json(content)
    except (ValidationError, JSONDecodeError) as e:
        raise HTTPException(status_code=502, detail=f'LLM returned invalid response: {e}')
