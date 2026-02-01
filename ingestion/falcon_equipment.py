from models import PolicyRule, LenderProgram
from utils.enums import PolicyWeight
from models import Lender, LenderProgram
from database.session import SessionLocal

db = SessionLocal()

# 1. Create Lender
lender = Lender(
    name="Falcon Equipment Finance",
    contact_name="Emma Tickner",
    contact_email="ETickner@FalconEquipmentFinance.com",
    contact_phone="651-332-6517",
)
db.add(lender)
db.commit()
db.refresh(lender)

# 2. Create Lender Program
program = LenderProgram(
    lender_id=lender.id, name="Falcon Equipment Finance Program 2025"
)
db.add(program)
db.commit()
db.refresh(program)

rules_data = [
    {
        "rule_type": "min_fico",
        "operator": ">=",
        "value": 680,
        "weight": PolicyWeight.HIGH,
        "is_hard": True,
    },
    {
        "rule_type": "min_paynet",
        "operator": ">=",
        "value": 660,
        "weight": PolicyWeight.HIGH,
        "is_hard": True,
    },
    {
        "rule_type": "min_years_in_business",
        "operator": ">=",
        "value": 3,
        "weight": PolicyWeight.MEDIUM,
        "is_hard": True,
    },
    {
        "rule_type": "max_age_truck",
        "operator": "<=",
        "value": 10,
        "weight": PolicyWeight.MEDIUM,
        "is_hard": True,
    },
    {
        "rule_type": "max_age_reefer_trailer",
        "operator": "<=",
        "value": 7,
        "weight": PolicyWeight.MEDIUM,
        "is_hard": True,
    },
    {
        "rule_type": "min_truck_count",
        "operator": ">=",
        "value": 5,
        "weight": PolicyWeight.MEDIUM,
        "is_hard": True,
    },
    {
        "rule_type": "max_loan_trucking_app",
        "operator": "<=",
        "value": 150000,
        "weight": PolicyWeight.MEDIUM,
        "is_hard": True,
    },
    {
        "rule_type": "max_loan_commercial_app",
        "operator": "<=",
        "value": 250000,
        "weight": PolicyWeight.MEDIUM,
        "is_hard": True,
    },
    {
        "rule_type": "max_loan_manufacturing_app",
        "operator": "<=",
        "value": 350000,
        "weight": PolicyWeight.MEDIUM,
        "is_hard": True,
    },
    {
        "rule_type": "max_additional_loan",
        "operator": "<=",
        "value": 100000,
        "weight": PolicyWeight.LOW,
        "is_hard": False,
    },
    {
        "rule_type": "max_total_loan",
        "operator": "<=",
        "value": 350000,
        "weight": PolicyWeight.LOW,
        "is_hard": False,
    },
]

for r in rules_data:
    rule = PolicyRule(program_id=program.id, **r)
    db.add(rule)

db.commit()
print("Falcon Equipment Finance rules added successfully.")
