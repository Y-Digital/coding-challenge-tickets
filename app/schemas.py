from enum import Enum

from pydantic import BaseModel, Field


# ── Request ──────────────────────────────────────────────────────

class CustomerTier(str, Enum):
    enterprise = "enterprise"
    business = "business"
    free = "free"


class TicketInput(BaseModel):
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    customer_tier: CustomerTier


# ── Response ─────────────────────────────────────────────────────

class TriageCategory(str, Enum):
    billing = "billing"
    bug = "bug"
    feature_request = "feature_request"
    security = "security"
    other = "other"


class TriagePriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TriageResult(BaseModel):
    category: TriageCategory
    priority: TriagePriority
    summary: str
    actions: list[str]
    confidence: float = Field(..., ge=0.0, le=1.0)
