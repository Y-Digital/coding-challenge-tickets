"""
Test 1: API input validation — ensure the endpoint rejects bad input.

TODO (candidate): add more edge-case validations as you see fit.
"""


def test_triage_rejects_empty_subject(client):
    """POST /triage with an empty subject should return 422."""
    resp = client.post(
        "/triage",
        json={"subject": "", "body": "some body", "customer_tier": "free"},
    )
    assert resp.status_code == 422


def test_triage_rejects_missing_body(client):
    """POST /triage without a body field should return 422."""
    resp = client.post(
        "/triage",
        json={"subject": "Help", "customer_tier": "enterprise"},
    )
    assert resp.status_code == 422


def test_triage_rejects_invalid_tier(client):
    """POST /triage with an unknown customer_tier should return 422."""
    resp = client.post(
        "/triage",
        json={"subject": "Help", "body": "details", "customer_tier": "platinum"},
    )
    assert resp.status_code == 422
