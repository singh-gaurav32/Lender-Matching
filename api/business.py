from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from debs import get_db
from models import Business, PersonalGuarantor, BusinessCredit
from api.schemas import BusinessCreate, BusinessOut

router = APIRouter()


@router.post("/", response_model=BusinessOut)
def create_business(business_in: BusinessCreate, db: Session = Depends(get_db)):
    # Basic validations
    if business_in.years_in_business <= 0:
        raise HTTPException(status_code=400, detail="Years in business must be > 0")
    if business_in.annual_revenue < 0:
        raise HTTPException(status_code=400, detail="Annual revenue cannot be negative")
    if not (300 <= business_in.guarantor.fico_score <= 850):
        raise HTTPException(status_code=400, detail="Guarantor FICO score invalid")
    if business_in.credit.paynet_score < 0:
        raise HTTPException(status_code=400, detail="PayNet score cannot be negative")

    business = Business(
        legal_name=business_in.legal_name,
        industry=business_in.industry,
        state=business_in.state,
        years_in_business=business_in.years_in_business,
        annual_revenue=business_in.annual_revenue,
    )
    db.add(business)
    db.commit()
    db.refresh(business)

    g = PersonalGuarantor(business_id=business.id, **business_in.guarantor.model_dump())
    c = BusinessCredit(business_id=business.id, **business_in.credit.model_dump())
    db.add_all([g, c])
    db.commit()
    return business
