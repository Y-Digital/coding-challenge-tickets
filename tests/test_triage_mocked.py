"""
Test 2: Triage with mocked LLM — deterministic behaviour.

TODO (candidate): extend with more assertions or scenarios.
"""


def test_triage_returns_valid_result(client):
    """POST /triage with valid input should return a well-formed TriageResult."""
    resp = client.post(
        "/triage",
        json={
            "subject": "App crashes on upload",
            "body": "Uploading a large file causes a white screen.",
            "customer_tier": "business",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "bug"
    assert data["priority"] == "high"
    assert 0.0 <= data["confidence"] <= 1.0
    assert isinstance(data["actions"], list)


def test_batch_triage_returns_list(client):
    """POST /batch-triage should return one result per ticket."""
    tickets = [
        {
            "subject": "Billing issue",
            "body": "Double charged.",
            "customer_tier": "enterprise",
        },
        {
            "subject": "Feature request",
            "body": "Need dark mode.",
            "customer_tier": "free",
        },
    ]
    resp = client.post("/batch-triage", json=tickets)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
