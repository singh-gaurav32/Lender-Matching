import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_lender():
    resp = client.post(
        "/lenders",
        json={
            "name": "ABC Bank",
            "type": "bank"
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "ABC Bank"
    assert "id" in data


def test_add_lender_rule():
    lender = client.post(
        "/lenders",
        json={"name": "XYZ Finance", "type": "nbfc"},
    ).json()

    resp = client.post(
        f"/lenders/{lender['id']}/rules",
        json={
            "rule_type": "fico",
            "operator": ">=",
            "value": 700,
        },
    )
    assert resp.status_code == 201
    rule = resp.json()
    assert rule["rule_type"] == "fico"
    assert rule["value"] == 700


def test_prevent_duplicate_rule():
    lender = client.post(
        "/lenders",
        json={"name": "Dup Rule Bank", "type": "bank"},
    ).json()

    payload = {
        "rule_type": "paynet",
        "operator": ">=",
        "value": 75,
    }

    first = client.post(f"/lenders/{lender['id']}/rules", json=payload)
    assert first.status_code == 201

    second = client.post(f"/lenders/{lender['id']}/rules", json=payload)
    assert second.status_code == 400


def test_update_lender_rule():
    lender = client.post(
        "/lenders",
        json={"name": "Rule Update Bank", "type": "bank"},
    ).json()

    rule = client.post(
        f"/lenders/{lender['id']}/rules",
        json={
            "rule_type": "loan_amount",
            "operator": "<=",
            "value": 500000,
        },
    ).json()

    resp = client.put(
        f"/lenders/{lender['id']}/rules/{rule['id']}",
        json={"value": 750000},
    )

    assert resp.status_code == 200
    assert resp.json()["value"] == 750000
