# api/schemas.py
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional, List, Dict

# -------- Business --------
class BusinessCreate(BaseModel):
    legal_name: str
    industry: str
    state: str
    years_in_business: int = Field(ge=0)
    annual_revenue: float = Field(gt=0)
    pan: str  # business uniqueness (India)


class BusinessOut(BusinessCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )


# -----------------------------
# Personal Guarantor
# -----------------------------
class PersonalGuarantorCreate(BaseModel):
    fico_score: int
    has_bankruptcy: Optional[bool] = False
    has_tax_liens: Optional[bool] = False

class PersonalGuarantorOut(PersonalGuarantorCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )

# -----------------------------
# Business Credit
# -----------------------------
class BusinessCreditCreate(BaseModel):
    paynet_score: float
    trade_line_count: Optional[int] = 0

class BusinessCreditOut(BusinessCreditCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )

# -----------------------------
# Business / Borrower
# -----------------------------
class BusinessCreate(BaseModel):
    legal_name: str
    industry: str
    state: str
    years_in_business: int
    annual_revenue: float
    guarantor: PersonalGuarantorCreate
    credit: BusinessCreditCreate

class BusinessOut(BusinessCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )