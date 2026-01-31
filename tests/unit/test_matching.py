# tests/unit/test_matching.py
import pytest
from services.matching import MatchingService
from models.loan_request import LoanRequest
from models.lender_policy import LenderProgram, PolicyRule
from models.match_result import MatchResult, RuleResult
from utils.enums import FeatureType


from models.business import Business, BusinessFeature
from models.loan_request import LoanRequest
from models import BusinessCredit, MatchResult
from models import PersonalGuarantor
from utils.enums import FeatureType, PolicyWeight

@pytest.fixture
def loan_with_business(db_session):
    # create actual business
    business = Business(
        legal_name="Test Corp",
        industry="Manufacturing",
        state="NY",
        years_in_business=5,
        annual_revenue=500000,
    )
    db_session.add(business)
    db_session.flush()  # assigns id

    # optional: add credit info
    credit = BusinessCredit(
        business_id=business.id,
        paynet_score=750,
        trade_line_count=3
    )
    guarantor = PersonalGuarantor(
        business_id=business.id,
        fico_score=720,
        has_bankruptcy=False,
        has_tax_liens=False
    )
    db_session.add_all([credit, guarantor])

    # create loan request
    loan = LoanRequest(
        business_id=business.id,
        amount=100000,
        term_months=36,
        equipment_type="Tractor",
        equipment_year=2018
    )
    db_session.add(loan)
    features = [
        BusinessFeature(business_id=business.id, feature_type=FeatureType.FICO, value=720),
        BusinessFeature(business_id=business.id, feature_type=FeatureType.YEARS_IN_BUSINESS, value=5),
        BusinessFeature(business_id=business.id, feature_type=FeatureType.REVENUE, value=500000),
    ]
    db_session.add_all(features)
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


def test_matching_all_rules_pass(db_session, loan_with_business, lender_program):
    service = MatchingService(db_session)

    results = service.match_loan(loan_with_business.id)

    assert len(results) == 1
    result: MatchResult = results[0]

    assert result.eligible is True
    assert result.fit_score == 80
    assert result.summary == []


def test_matching_rule_fails(db_session, loan_with_business, lender_program):
    # break fico
    loan_with_business.business.features[0].value = 650
    db_session.commit()

    service = MatchingService(db_session)
    results = service.match_loan(loan_with_business.id)

    result = results[0]
    assert result.eligible is False
    assert result.fit_score == 30.0
    assert "fico" in result.summary[0]


def test_missing_feature_fails(db_session, loan_with_business, lender_program):
    loan_with_business.business.features = []  # no features
    db_session.commit()
    service = MatchingService(db_session)
    results = service.match_loan(loan_with_business.id)

    result = results[0]
    assert result.eligible is False
    assert result.fit_score == 0
    assert "feature missing" in result.summary[0]
