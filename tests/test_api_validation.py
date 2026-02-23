"""
Test: API input validation — the endpoint should reject bad input.

TODO (candidate): add more edge-case validations as you see fit.
"""


def test_triage_rejects_empty_subject(client):
    resp = client.post(
        "/triage",
        json={"subject": "", "body": "some body", "customer_tier": "free"},
    )
    assert resp.status_code == 422


def test_triage_rejects_missing_body(client):
    resp = client.post(
        "/triage",
        json={"subject": "Help", "customer_tier": "enterprise"},
    )
    assert resp.status_code == 422


def test_triage_rejects_invalid_tier(client):
    resp = client.post(
        "/triage",
        json={"subject": "Help", "body": "details", "customer_tier": "platinum"},
    )
    assert resp.status_code == 422
