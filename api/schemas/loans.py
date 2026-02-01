from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from utils.enums import LoanStatus


class LoanCreate(BaseModel):
    business_id: int
    amount: float = Field(gt=0)
    term_months: int = Field(gt=0)
    equipment_type: str
    equipment_year: int


class LoanOut(LoanCreate):
    id: int
    status: LoanStatus

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )




# -----------------------------
# Loan Request
# -----------------------------
class LoanRequestCreate(BaseModel):
    business_id: int
    amount: float
    term_months: int
    equipment_type: str
    equipment_year: int

class LoanRequestOut(LoanRequestCreate):
    id: int
    status: LoanStatus
    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )
