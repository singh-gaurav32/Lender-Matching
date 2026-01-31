from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

# -------- Lender --------
class LenderCreate(BaseModel):
    name: str
    is_active: bool = True


class LenderOut(LenderCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )


# -------- Lender Rules --------
class RuleCreate(BaseModel):
    rule_type: str          # use enums.RuleType
    operator: str           # >=, <=, ==, in
    value: str              # stored raw, interpreted later


class RuleOut(RuleCreate):
    id: int
    lender_id: int

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )


# api/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional


# -------- Lender Program --------
class LenderProgramCreate(BaseModel):
    lender_id: int
    name: str
    description: Optional[str] = None
    is_active: bool = True


class LenderProgramOut(LenderProgramCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )


# -------- Policy Rule --------
class PolicyRuleCreate(BaseModel):
    program_id: int
    rule_type: str   # use enums.RuleType
    operator: str    # >=, <=, in, not_in
    value: str       # store raw; parsed later
    weight: float = 1.0


class PolicyRuleOut(PolicyRuleCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )


# -------- Optional: Nested Output --------
class LenderProgramWithRulesOut(LenderProgramOut):
    rules: List[PolicyRuleOut] = []
