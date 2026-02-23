"""
Entry-point for the AI Text Triage API.

TODO: Replace the placeholder LLM client with AzureOpenAIClient.
"""

import logging

from fastapi import FastAPI

from app.config import settings
from app.routers.triage import router as triage_router
from app.services.llm_client import AzureOpenAIClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(
    title="AI Text Triage API",
    version="0.1.0",
    description="Triage support tickets using an LLM.",
)

app.include_router(triage_router)


@app.on_event("startup")
async def _startup():
    app.state.llm_client = AzureOpenAIClient(
        endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        deployment=settings.azure_openai_deployment,
        api_version=settings.azure_openai_api_version,
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
