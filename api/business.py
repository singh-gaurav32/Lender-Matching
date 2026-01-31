from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from debs import get_db
from models import Business, PersonalGuarantor, BusinessCredit
from api.schemas import BusinessCreate, BusinessOut

router = APIRouter()

# # -----------------------------
# # Create business
# # -----------------------------
# @router.post("/", response_model=BusinessOut)
# def create_business(business_in: BusinessCreate, db: Session = Depends(get_db)):
#     # Basic validations
#     if business_in.years_in_business <= 0:
#         raise HTTPException(status_code=400, detail="Years in business must be > 0")
#     if business_in.annual_revenue < 0:
#         raise HTTPException(status_code=400, detail="Annual revenue cannot be negative")
#     if not (300 <= business_in.guarantor.fico_score <= 850):
#         raise HTTPException(status_code=400, detail="Guarantor FICO score invalid")
#     if business_in.credit.paynet_score < 0:
#         raise HTTPException(status_code=400, detail="PayNet score cannot be negative")

#     business = Business(
#         legal_name=business_in.legal_name,
#         industry=business_in.industry,
#         state=business_in.state,
#         years_in_business=business_in.years_in_business,
#         annual_revenue=business_in.annual_revenue
#     )
#     db.add(business)
#     db.commit()
#     db.refresh(business)

#     g = PersonalGuarantor(business_id=business.id, **business_in.guarantor.dict())
#     c = BusinessCredit(business_id=business.id, **business_in.credit.dict())
#     db.add_all([g, c])
#     db.commit()
#     return business

# # -----------------------------
# # Get business
# # -----------------------------
# @router.get("/{business_id}", response_model=BusinessOut)
# def get_business(business_id: int, db: Session = Depends(get_db)):
#     business = db.get(Business, business_id)
#     if not business:
#         raise HTTPException(status_code=404, detail="Business not found")
#     return business

# # -----------------------------
# # Update business
# # -----------------------------
# @router.put("/{business_id}", response_model=BusinessOut)
# def update_business(business_id: int, business_in: BusinessCreate, db: Session = Depends(get_db)):
#     business = db.get(Business, business_id)
#     if not business:
#         raise HTTPException(status_code=404, detail="Business not found")

#     for field, value in business_in.dict(exclude={"guarantor", "credit"}).items():
#         setattr(business, field, value)

#     # Update nested guarantor
#     for field, value in business_in.guarantor.dict().items():
#         setattr(business.guarantor, field, value)

#     # Update nested credit
#     for field, value in business_in.credit.dict().items():
#         setattr(business.credit, field, value)

#     db.commit()
#     db.refresh(business)
#     return business

# # -----------------------------
# # Delete business
# # -----------------------------
# @router.delete("/{business_id}")
# def delete_business(business_id: int, db: Session = Depends(get_db)):
#     business = db.get(Business, business_id)
#     if not business:
#         raise HTTPException(status_code=404, detail="Business not found")
#     db.delete(business)
#     db.commit()
#     return {"detail": "Business deleted"}
