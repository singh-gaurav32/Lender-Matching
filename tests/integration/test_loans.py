# tests/integration/test_loan_request.py

import pytest
from models import (
    Business, PersonalGuarantor, BusinessCredit, LoanRequest,
    PolicyRule,LenderProgram
)
from utils.enums import LoanStatus, PolicyWeight

@pytest.fixture
def business(db_session):
    db = db_session
    b = Business(
        legal_name="Test Pvt Ltd",
        industry="Manufacturing",
        state="KA",
        years_in_business=5,
        annual_revenue=1_000_000.0,
    )
    db.add(b)
    db.commit()
    db.refresh(b)

    g = PersonalGuarantor(
        business_id=b.id,
        fico_score=720,
        has_bankruptcy=False,
        has_tax_liens=False,
    )

    c = BusinessCredit(
        business_id=b.id,
        paynet_score=80.5,
        trade_line_count=10,
    )

    db.add_all([g, c])
    db.commit()
    db.refresh(b)

    return b

@pytest.fixture
def loan_request(db_session, business):
    loan = LoanRequest(
        business_id=business.id,
        amount=500000,
        term_months=36,
        equipment_type="excavator",
        equipment_year=2022,
        status=LoanStatus.DRAFT,
    )
    db_session.add(loan)
    db_session.commit()
    db_session.refresh(loan)
    return loan

@pytest.fixture
def lender_program(db_session):
    program = LenderProgram(id=1, lender_id=1, name="TestLender")

    rule1 = PolicyRule(
        id=1,
        rule_type="fico",
        operator=">=",
        value=700,
        weight=PolicyWeight.HIGH,
    )

    rule2 = PolicyRule(
        id=2,
        rule_type="time_in_business",
        operator=">=",
        value=3,
        weight=PolicyWeight.MEDIUM,
    )

    program.rules = [rule1, rule2]
    db_session.add(program)
    db_session.commit()
    return program



def test_create_loan(client, business:Business):
    payload = {
        "business_id": business.id,
        "amount": 500000,
        "term_months": 36,
        "equipment_type": "excavator",
        "equipment_year": 2021,
    }

    resp = client.post("/loans/", json=payload)

    assert resp.status_code == 200
    data = resp.json()

    assert data["id"] is not None
    assert data["business_id"] == business.id
    assert data["amount"] == 500000
    assert data["term_months"] == 36
    assert data["equipment_type"] == "excavator"
    assert data["equipment_year"] == 2021
    assert data["status"] == "draft"

def test_initiate_match_actual_run(client, loan_request, db_session, lender_program):
    assert loan_request.status == LoanStatus.DRAFT
    programs = db_session.query(LenderProgram).all()
    if not programs:
        raise RuntimeError("No lender programs configured")

    resp = client.post(
        "/loans/initiate_match",
        params={"loan_request_id": loan_request.id},
    )

    assert resp.status_code == 200
    assert resp.json() == "Loan Matching Initiated"

    db_session.refresh(loan_request)

    assert loan_request.status in (
        LoanStatus.PROCESSING,
        LoanStatus.COMPLETED,
        LoanStatus.SUBMITTED,
    )

    from models import BusinessFeature, MatchResult

    features = (
        db_session.query(BusinessFeature)
        .filter(BusinessFeature.business_id == loan_request.business_id)
        .all()
    )
    assert len(features) > 0

    matches = (
        db_session.query(MatchResult)
        .filter(MatchResult.loan_request_id == loan_request.id)
        .all()
    )
    
    assert len(matches) > 0
    first_match = matches[0]
    assert first_match.eligible == True
    assert first_match.fit_score == 80.0



