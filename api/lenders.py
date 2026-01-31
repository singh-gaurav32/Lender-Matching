from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from debs import get_db
from models import Lender, LenderProgram, PolicyRule
from api.schemas import LenderCreate, LenderOut, LenderProgramCreate, PolicyRuleCreate

router = APIRouter()

# # -----------------------------
# # Create Lender
# # -----------------------------
# @router.post("/", response_model=LenderOut)
# def create_lender(lender_in: LenderCreate, db: Session = Depends(get_db)):
#     lender = Lender(name=lender_in.name)
#     db.add(lender)
#     db.commit()
#     db.refresh(lender)
#     return lender

# # -----------------------------
# # Add Program to Lender
# # -----------------------------
# @router.post("/{lender_id}/programs", response_model=LenderOut)
# def add_program(lender_id: int, program_in: LenderProgramCreate, db: Session = Depends(get_db)):
#     lender = db.get(Lender, lender_id)
#     if not lender:
#         raise HTTPException(status_code=404, detail="Lender not found")
#     program = LenderProgram(lender_id=lender.id, name=program_in.name)
#     db.add(program)
#     db.commit()
#     db.refresh(lender)
#     return lender

# # -----------------------------
# # Add Rules to Program
# # -----------------------------
# @router.post("/programs/{program_id}/rules", response_model=LenderOut)
# def add_rules(program_id: int, rules_in: list[PolicyRuleCreate], db: Session = Depends(get_db)):
#     program = db.get(LenderProgram, program_id)
#     if not program:
#         raise HTTPException(status_code=404, detail="Program not found")

#     for rule_in in rules_in:
#         # Check if same rule_type already exists in this program
#         exists = (
#             db.query(PolicyRule)
#             .filter(
#                 PolicyRule.program_id == program.id,
#                 PolicyRule.rule_type == rule_in.rule_type
#             )
#             .first()
#         )
#         if exists:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Rule '{rule_in.rule_type}' already exists for this program"
#             )

#         rule = PolicyRule(
#             program_id=program.id,
#             rule_type=rule_in.rule_type,
#             operator=rule_in.operator,
#             value=rule_in.value,
#             weight=rule_in.weight
#         )
#         db.add(rule)

#     db.commit()
#     db.refresh(program)
#     return program

# @router.post("/programs/{program_id}/rule", response_model=PolicyRule)
# def add_single_rule(program_id: int, rule_in: PolicyRuleCreate, db: Session = Depends(get_db)):
#     program = db.get(LenderProgram, program_id)
#     if not program:
#         raise HTTPException(status_code=404, detail="Program not found")

#     # Check if rule_type already exists
#     exists = (
#         db.query(PolicyRule)
#         .filter(PolicyRule.program_id == program.id, PolicyRule.rule_type == rule_in.rule_type)
#         .first()
#     )
#     if exists:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Rule '{rule_in.rule_type}' already exists for this program"
#         )

#     rule = PolicyRule(
#         program_id=program.id,
#         rule_type=rule_in.rule_type,
#         operator=rule_in.operator,
#         value=rule_in.value,
#         weight=rule_in.weight
#     )
#     db.add(rule)
#     db.commit()
#     db.refresh(rule)
#     return rule


# # -----------------------------
# # Modify Rule
# # -----------------------------
# @router.put("/rules/{rule_id}", response_model=PolicyRule)
# def update_rule(rule_id: int, rule_in: PolicyRuleCreate, db: Session = Depends(get_db)):
#     rule = db.get(PolicyRule, rule_id)
#     if not rule:
#         raise HTTPException(status_code=404, detail="Rule not found")
#     rule.rule_type = rule_in.rule_type
#     rule.operator = rule_in.operator
#     rule.value = rule_in.value
#     rule.weight = rule_in.weight
#     db.commit()
#     db.refresh(rule)
#     return rule
