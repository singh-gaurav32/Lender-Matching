from db import SessionLocal
from models import Lender, LenderProgram, PolicyRule

db = SessionLocal()

# -----------------------------
# LENDER
# -----------------------------
lender = Lender(
    name="Credit Box Partner Lender",
)
db.add(lender)
db.flush()

# -----------------------------
# PROGRAM
# -----------------------------
program = LenderProgram(
    lender_id=lender.id,
    name="Credit Box – Tiered Program",
)
db.add(program)
db.flush()

# -----------------------------
# POLICY RULES
# -----------------------------
rules = [
    # -------- Tier Guidelines ----------
    {
        "rule_type": "credit_tiers",
        "operator": "json",
        "value": {
            "tier_1": {"fico": 725, "tib": 3, "paynet": 685},
            "tier_2": {"fico": 710, "tib": 3, "paynet": 675},
            "tier_3": {"fico": 700, "tib": 2, "paynet": 665},
        },
        "is_hard": False,
    },
    # -------- No PayNet ----------
    {
        "rule_type": "no_paynet_tiers",
        "operator": "json",
        "value": {
            "tier_1": {"fico": 735, "tib": 5},
            "tier_2": {"fico": 720, "tib": 3},
            "tier_3": {"fico": 710, "tib": 2},
        },
        "is_hard": False,
    },
    # -------- Corp Only ----------
    {
        "rule_type": "corp_only_tiers",
        "operator": "json",
        "value": {
            "tier_1": {"paynet": 700, "tib": 10},
            "tier_2": {"paynet": 690, "tib": 5},
            "tier_3": {"paynet": 680, "tib": 5},
        },
        "is_hard": False,
    },
    # -------- Bankruptcy ----------
    {
        "rule_type": "bankruptcy_years",
        "operator": ">=",
        "value": 7,
        "is_hard": True,
    },
    # -------- Comparable Debt ----------
    {
        "rule_type": "comparable_debt",
        "operator": "json",
        "value": {
            "open_trade": ">= requested_amount",
            "closed_trade_months": 12,
            "min_contracts": 3,
            "min_contract_amount": 10000,
        },
        "is_hard": False,
    },
    # -------- Revolving Debt ----------
    {
        "rule_type": "revolving_debt_limit",
        "operator": "json",
        "value": {
            "personal_revolving": 30000,
            "revolving_plus_unsecured": 50000,
            "exclude": ["student_loans"],
        },
        "is_hard": False,
    },
    # -------- Restricted Industries ----------
    {
        "rule_type": "industry_blacklist",
        "operator": "not_in",
        "value": [
            "Gaming/Gambling",
            "Foreign Country",
            "Aesthetic",
            "Hazmat",
            "No Physical Location",
            "Real Estate",
            "Oil & Gas",
            "Weapons/Firearms",
            "OTR",
            "MSBs",
            "Beauty/Tanning Salons",
            "Restaurants",
            "Adult Entertainment",
            "Tattoo/Piercing",
            "Car Wash",
            "Non-Essential Use",
        ],
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
