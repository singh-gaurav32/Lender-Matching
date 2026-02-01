rules = [
    # Hard rules
    {
        "rule_type": "business_time_in_business",
        "operator": ">=",
        "value": 2,
        "is_hard": True,
        "weight": 3,
    },
    {
        "rule_type": "credit_score",
        "operator": ">=",
        "value": 700,
        "is_hard": True,
        "weight": 3,
    },
    {
        "rule_type": "personal_guarantor_required",
        "operator": "==",
        "value": True,
        "is_hard": True,
        "weight": 3,
    },
    {
        "rule_type": "homeownership_required",
        "operator": "==",
        "value": True,
        "is_hard": True,
        "weight": 2,
    },
    {
        "rule_type": "CDL_required",
        "operator": "==",
        "value": True,
        "is_hard": True,
        "weight": 2,
    },
    {
        "rule_type": "bankruptcy_discharge",
        "operator": ">=",
        "value": 5,
        "is_hard": True,
        "weight": 3,
    },
    {
        "rule_type": "citizens_state_exclusion",
        "operator": "not_in",
        "value": ["California"],
        "is_hard": True,
        "weight": 3,
    },
    {
        "rule_type": "cannabis_business",
        "operator": "==",
        "value": False,
        "is_hard": True,
        "weight": 3,
    },
    # Soft rules
    {
        "rule_type": "mileage_limit",
        "operator": "<=",
        "value": 500000,
        "is_hard": False,
        "weight": 2,
    },
    {
        "rule_type": "equipment_age",
        "operator": "<=",
        "value": 10,
        "is_hard": False,
        "weight": 2,
    },
    {
        "rule_type": "equipment_type",
        "operator": "in",
        "value": [
            "Class 8 Truck",
            "Medium Duty Truck",
            "Light Duty Truck",
            "Construction Equipment",
        ],
        "is_hard": False,
        "weight": 2,
    },
    {
        "rule_type": "insurance_required",
        "operator": "==",
        "value": True,
        "is_hard": False,
        "weight": 1,
    },
    {
        "rule_type": "private_party_transaction_allowed",
        "operator": "==",
        "value": False,
        "is_hard": False,
        "weight": 1,
    },
]
from models import Lender, LenderProgram, PolicyRule
from database.session import SessionLocal

db = SessionLocal()

# Create Lender
lender = Lender(
    name="Citizens Bank",
    contact_person="Joey Walter",
    email="joey.walter@thecitizensbank.net",
    phone="501-451-5113",
)
db.add(lender)
db.commit()
db.refresh(lender)

# Create Lender Program
program = LenderProgram(lender_id=lender.id, name="Equipment Finance Program 2025")
db.add(program)
db.commit()
db.refresh(program)

# Now you can add rules using program.id
print(f"Lender ID: {lender.id}, Program ID: {program.id}")

# Example loop to create PolicyRule objects
policy_rules = []
for r in rules:
    policy_rules.append(PolicyRule(program_id=program.id, **r))

db.add_all(policy_rules)
db.commit()
