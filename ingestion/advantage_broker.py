from database.session import SessionLocal
from models import Lender, LenderProgram, PolicyRule
from utils.enums import PolicyWeight

db = SessionLocal()

# -------------------------
# Create Lender
# -------------------------
lender = Lender(
    name="Advantage+ Financing",
    contact_name="Sales Support",
    contact_email="SalesSupport@advantageplusfinancing.com",
    contact_phone="262-439-7600",
)
db.add(lender)
db.commit()
db.refresh(lender)

# -------------------------
# Create Program
# -------------------------
program = LenderProgram(
    lender_id=lender.id,
    name="Non-Trucking Program ≤ $75,000",
)
db.add(program)
db.commit()
db.refresh(program)

# -------------------------
# Policy Rules
# -------------------------
rules = [
    # Core eligibility
    dict(
        rule_type="min_fico",
        operator=">=",
        value=680,
        is_hard=True,
        weight=PolicyWeight.HIGH,
    ),
    dict(
        rule_type="min_fico_startup",
        operator=">=",
        value=700,
        is_hard=True,
        weight=PolicyWeight.HIGH,
    ),
    dict(
        rule_type="min_years_in_business",
        operator=">=",
        value=3,
        is_hard=True,
        weight=PolicyWeight.MEDIUM,
    ),
    # Loan constraints
    dict(
        rule_type="min_loan_amount",
        operator=">=",
        value=10_000,
        is_hard=True,
        weight=PolicyWeight.MEDIUM,
    ),
    dict(
        rule_type="max_loan_amount",
        operator="<=",
        value=75_000,
        is_hard=True,
        weight=PolicyWeight.HIGH,
    ),
    dict(
        rule_type="max_term_months",
        operator="<=",
        value=60,
        is_hard=False,
        weight=PolicyWeight.LOW,
    ),
    # Down payment
    dict(
        rule_type="min_down_payment_pct",
        operator=">=",
        value=10,
        is_hard=False,
        weight=PolicyWeight.LOW,
    ),
    dict(
        rule_type="startup_security_deposit_pct",
        operator=">=",
        value=10,
        is_hard=False,
        weight=PolicyWeight.LOW,
    ),
    # Credit history restrictions
    dict(
        rule_type="no_bankruptcy",
        operator="==",
        value=True,
        is_hard=True,
        weight=PolicyWeight.HIGH,
    ),
    dict(
        rule_type="no_judgements",
        operator="==",
        value=True,
        is_hard=True,
        weight=PolicyWeight.MEDIUM,
    ),
    dict(
        rule_type="no_foreclosures",
        operator="==",
        value=True,
        is_hard=True,
        weight=PolicyWeight.MEDIUM,
    ),
    dict(
        rule_type="no_repossessions",
        operator="==",
        value=True,
        is_hard=True,
        weight=PolicyWeight.MEDIUM,
    ),
    dict(
        rule_type="no_tax_liens",
        operator="==",
        value=True,
        is_hard=True,
        weight=PolicyWeight.MEDIUM,
    ),
    dict(
        rule_type="no_recent_collections",
        operator="==",
        value={"years": 3},
        is_hard=True,
        weight=PolicyWeight.MEDIUM,
    ),
    # Preferences (soft)
    dict(
        rule_type="preferred_trade_history_years",
        operator=">=",
        value=7,
        is_hard=False,
        weight=PolicyWeight.LOW,
    ),
    dict(
        rule_type="preferred_comparable_credit_pct",
        operator=">=",
        value=80,
        is_hard=False,
        weight=PolicyWeight.LOW,
    ),
    # Other constraints
    dict(
        rule_type="us_citizen_only",
        operator="==",
        value=True,
        is_hard=True,
        weight=PolicyWeight.HIGH,
    ),
]

for r in rules:
    db.add(PolicyRule(program_id=program.id, **r))

db.commit()

print(
    f"Created lender '{lender.name}', program '{program.name}', "
    f"and {len(rules)} policy rules successfully."
)
