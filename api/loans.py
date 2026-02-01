from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from debs import get_db
from models import LoanRequest, MatchResult
from api.schemas import LoanRequestCreate, LoanRequestOut, MatchResultOut
from enum import IntEnum
from models.loan_request import LoanStatus
from services.loan_workflow import LoanWorkflowService

router = APIRouter()


@router.post("/", response_model=LoanRequestOut)
def create_loan(loan_in: LoanRequestCreate, db: Session = Depends(get_db)):
    loan = LoanRequest(**loan_in.model_dump(), status=LoanStatus.DRAFT)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


@router.post("/initiate_match", response_model=str)
def initiate_match(
    loan_request_id: int,
    db: Session = Depends(get_db),
):
    loan = db.get(LoanRequest, loan_request_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status in (
        LoanStatus.PROCESSING,
        LoanStatus.COMPLETED,
        LoanStatus.SUBMITTED,
    ):
        raise HTTPException(status_code=404, detail="Already initiated")

    LoanWorkflowService.run(loan, db)
    return "Loan Matching Initiated"


@router.get("/{loan_id}/matches", response_model=list[MatchResultOut])
def get_loan_matches(loan_id: int, db: Session = Depends(get_db)):
    loan = db.get(LoanRequest, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.status == LoanStatus.DRAFT:
        raise HTTPException(
            status_code=400, detail="Loan not yet eligible for matching"
        )

    matches = db.query(MatchResult).filter(MatchResult.loan_request_id == loan_id).all()
    return matches
