from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from utils.enums import PolicyWeight

# -------- Lender --------
class LenderCreate(BaseModel):
    name: str
    # is_active: bool = True


class LenderOut(LenderCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )

# api/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional


# -------- Lender Program --------
class LenderProgramCreate(BaseModel):
    lender_id: int
    name: str


class LenderProgramOut(LenderProgramCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------- Policy Rule --------
class PolicyRuleCreate(BaseModel):
    program_id: int
    rule_type: str   # use enums.RuleType
    operator: str    # >=, <=, in, not_in
    value: Any
    weight: int = PolicyWeight.MEDIUM
    is_hard: bool = False

class PolicyRuleUpdate(BaseModel):
    rule_type: Optional[str] = None
    operator: Optional[str] = None
    value: Optional[Any] = None
    weight: Optional[int] = None
    is_hard: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class PolicyRuleOut(PolicyRuleCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


# -------- Optional: Nested Output --------
class LenderProgramWithRulesOut(LenderProgramOut):
    rules: List[PolicyRuleOut] = []
