from db import SessionLocal
from models import Lender, LenderProgram, PolicyRule

db = SessionLocal()

# -----------------------------
# LENDER
# -----------------------------
lender = Lender(
    name="Apex Commercial Capital",
    email="credit@apexcommercial.com",
)
db.add(lender)
db.flush()  # get lender.id

# -----------------------------
# LENDER PROGRAM
# -----------------------------
program = LenderProgram(
    lender_id=lender.id,
    name="Equipment & Medical Finance – PG",
    max_amount=500000,
    min_amount=10000,
    max_term_months=60,
)
db.add(program)
db.flush()  # get program.id

# -----------------------------
# POLICY RULES (JSON)
# -----------------------------
rules = [
    # -------- General ----------
    {
        "rule_type": "loan_amount",
        "operator": ">=",
        "value": 10000,
        "is_hard": True,
    },
    {
        "rule_type": "loan_amount",
        "operator": "<=",
        "value": 500000,
        "is_hard": True,
    },
    {
        "rule_type": "loan_term_months",
        "operator": "<=",
        "value": 60,
        "is_hard": True,
    },
    # -------- Credit ----------
    {
        "rule_type": "fico_score",
        "operator": ">=",
        "value": 640,
        "is_hard": True,
    },
    {
        "rule_type": "paynet_score",
        "operator": ">=",
        "value": 640,
        "is_hard": False,
    },
    # -------- Time in Business ----------
    {
        "rule_type": "years_in_business",
        "operator": ">=",
        "value": 2,
        "is_hard": True,
    },
    # -------- Bank Statements ----------
    {
        "rule_type": "bank_statements_months",
        "operator": ">=",
        "value": 3,
        "is_hard": True,
    },
    # -------- Geography ----------
    {
        "rule_type": "state_blacklist",
        "operator": "not_in",
        "value": ["CA", "NV", "ND", "VT"],
        "is_hard": True,
    },
    # -------- Equipment ----------
    {
        "rule_type": "equipment_age_years",
        "operator": "<=",
        "value": 15,
        "is_hard": True,
    },
    {
        "rule_type": "industry_blacklist",
        "operator": "not_in",
        "value": [
            "Cannabis",
            "Casino/Gambling",
            "Church/Non-profit",
            "Trucking",
            "Aircraft",
            "Boats",
            "ATMs",
        ],
        "is_hard": True,
    },
    # -------- Medical Program ----------
    {
        "rule_type": "medical_license_required",
        "operator": "==",
        "value": True,
        "is_hard": True,
    },
    {
        "rule_type": "licensed_profession",
        "operator": "in",
        "value": ["MD", "DO", "DDS", "DMD", "DVM", "OD", "DPM"],
        "is_hard": True,
    },
]

# -----------------------------
# INSERT RULES
# -----------------------------
for r in rules:
    db.add(
        PolicyRule(
            program_id=program.id,
            rule_type=r["rule_type"],
            operator=r["operator"],
            value=r["value"],
            is_hard=r.get("is_hard", False),
        )
    )

# -----------------------------
# COMMIT
# -----------------------------
db.commit()
db.close()
