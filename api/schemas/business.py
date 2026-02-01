# api/schemas.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class PersonalGuarantorCreate(BaseModel):
    fico_score: int
    has_bankruptcy: Optional[bool] = False
    has_tax_liens: Optional[bool] = False


class PersonalGuarantorOut(PersonalGuarantorCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --------------------------------------------


class BusinessCreditCreate(BaseModel):
    paynet_score: float
    trade_line_count: Optional[int] = 0


class BusinessCreditOut(BusinessCreditCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --------------------------------------------


class BusinessFeatureCreate(BaseModel):
    name: str
    value: str


class BusinessFeatureOut(BusinessFeatureCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


# -------------------------------------------


class BusinessCreate(BaseModel):
    legal_name: str
    industry: str
    state: str
    years_in_business: int = Field(ge=0)
    annual_revenue: float = Field(gt=0)
    guarantor: Optional[PersonalGuarantorCreate] = None
    credit: Optional[BusinessCreditCreate] = None


class BusinessOut(BusinessCreate):
    id: int
    guarantor: Optional[PersonalGuarantorOut] = None
    credit: Optional[BusinessCreditOut] = None

    model_config = ConfigDict(from_attributes=True)
