


def test_create_business(client):
    payload = {
        "legal_name": "Acme Pvt Ltd",
        "industry": "Manufacturing",
        "state": "KA",
        "years_in_business": 5,
        "annual_revenue": 1_000_000,
        "guarantor": {
            "fico_score": 720,
            "has_bankruptcy": False,
            "has_tax_liens": False
        },
        "credit": {
            "paynet_score": 85.5,
            "trade_line_count": 10
        }
    }

    resp = client.post("/businesses/", json=payload)

    assert resp.status_code == 200
    data = resp.json()

    assert "id" in data
    assert data["legal_name"] == payload["legal_name"]
    assert data["industry"] == payload["industry"]
    assert data["state"] == payload["state"]
    assert data["years_in_business"] == payload["years_in_business"]
    assert data["annual_revenue"] == payload["annual_revenue"]
