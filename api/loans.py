from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from debs import get_db
from models import LoanRequest, MatchResult
from api.schemas import LoanRequestCreate, LoanRequestOut
from enum import IntEnum

router = APIRouter()

# # -----------------------------
# # Status Enum
# # -----------------------------
# class LoanStatus(IntEnum):
#     PENDING = 0
#     UNDER_REVIEW = 1
#     APPROVED = 2
#     REJECTED = 3

# # -----------------------------
# # Create loan request
# # -----------------------------
# @router.post("/", response_model=LoanRequestOut)
# def create_loan(loan_in: LoanRequestCreate, db: Session = Depends(get_db)):
#     loan = LoanRequest(**loan_in.dict(), status=LoanStatus.PENDING)
#     db.add(loan)
#     db.commit()
#     db.refresh(loan)
#     return loan

# # -----------------------------
# # Get loan request by ID
# # -----------------------------
# @router.get("/{loan_id}", response_model=LoanRequestOut)
# def get_loan(loan_id: int, db: Session = Depends(get_db)):
#     loan = db.get(LoanRequest, loan_id)
#     if not loan:
#         raise HTTPException(status_code=404, detail="Loan not found")
#     return loan

# @router.get("/{loan_id}/matches", response_model=list[MatchResultOut])
# def get_loan_matches(loan_id: int, db: Session = Depends(get_db)):
#     loan = db.get(LoanRequest, loan_id)
#     if not loan:
#         raise HTTPException(status_code=404, detail="Loan not found")

#     if loan.status < 1:  # UNDER_REVIEW or higher
#         raise HTTPException(status_code=400, detail="Loan not yet eligible for matching")

#     matches = db.query(MatchResult).filter(MatchResult.loan_request_id == loan_id).all()
#     return matches

