

def test_create_lender(client):
    resp = client.post(
        "/lenders",
        json={
            "name": "ABC Bank",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "ABC Bank"
    assert "id" in data




def test_add_program_success(client):
    lender = client.post(
        "/lenders",
        json={"name": "XYZ Finance"},
    ).json()

    payload = {"name": "Program A", "lender_id":lender["id"]}

    res = client.post(f"lenders/{lender["id"]}/programs", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "id" in data
    assert data["lender_id"] == lender["id"]
    assert data["name"] == "Program A"
    

def test_add_lender_rules(client):
    lender = client.post(
        "/lenders",
        json={"name": "XYZ Finance", "type": "nbfc"},
    ).json()
    program_payload = {"name": "Program A", "lender_id":lender["id"]}

    program = client.post(f"lenders/{lender["id"]}/programs", json=program_payload).json()

    rules_payload = [
        {
            "program_id": program["id"],
            "rule_type": "fico",
            "operator": ">=",
            "value": "700",
            "weight": 3
        }
    ]

    resp = client.post(
        f"/lenders/programs/{program['id']}/rules",
        json=rules_payload,
    )
    assert resp.status_code == 200
    data = resp.json()
    rules = data["rules"]
    assert program["id"] == data["id"]
    assert rules[0]["rule_type"] == "fico"


# def test_prevent_duplicate_rule():
#     lender = client.post(
#         "/lenders",
#         json={"name": "Dup Rule Bank", "type": "bank"},
#     ).json()

#     payload = {
#         "rule_type": "paynet",
#         "operator": ">=",
#         "value": 75,
#     }

#     first = client.post(f"/lenders/{lender['id']}/rules", json=payload)
#     assert first.status_code == 201

#     second = client.post(f"/lenders/{lender['id']}/rules", json=payload)
#     assert second.status_code == 400


def test_update_lender_rule(client):
    lender = client.post(
        "/lenders",
        json={"name": "XYZ Finance", "type": "nbfc"},
    ).json()
    program_payload = {"name": "Program A", "lender_id":lender["id"]}

    program = client.post(f"lenders/{lender["id"]}/programs", json=program_payload).json()

    rules_payload = [
        {
            "program_id": program["id"],
            "rule_type": "fico",
            "operator": ">=",
            "value": "700",
            "weight": 3
        }
    ]

    resp = client.post(
        f"/lenders/programs/{program['id']}/rules",
        json=rules_payload,
    )
    data = resp.json()
    rule = data["rules"][0]
    resp = client.put(
        f"/lenders/rules/{rule['id']}",
        json={"value": 750000},
    )
    

    assert resp.status_code == 200
    assert resp.json()["value"] == 750000
