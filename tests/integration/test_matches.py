
import pytest
from models import (
    Business, PersonalGuarantor, BusinessCredit, LoanRequest,
    PolicyRule,LenderProgram,
    BusinessFeature, MatchResult
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


@pytest.fixture
def business_feature(db_session, loan_request):
    feature = BusinessFeature(
        loan_request_id=loan_request.id,
        key="fico_score",
        value=720
    )
    db_session.add(feature)
    db_session.commit()
    db_session.refresh(feature)
    return feature


@pytest.fixture
def match_result(db_session, loan_request, lender_program):
    result = MatchResult(
        loan_request_id=loan_request.id,
        lender_id=1,
        program_id=lender_program.id,
        fit_score=95.0,
        eligible=True
    )
    db_session.add(result)
    db_session.commit()
    db_session.refresh(result)
    return result


def test_get_loan_matches(client, db_session, loan_request, match_result):
    from utils.enums import LoanStatus
    loan_request.status = LoanStatus.PROCESSING
    match_result.loan_request_id = loan_request.id
    loan_request.business
    db_session.commit() 

    resp = client.get(f"/loans/{loan_request.id}/matches")

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0

    match = data[0]
    assert match["loan_request_id"] == loan_request.id
    assert match["lender_id"] == match_result.lender_id
    assert match["eligible"] is True
    assert "fit_score" in match
