from models import LoanRequest
from services.features import FeatureService
from services.matching import MatchingService
from debs import get_db
from sqlalchemy.orm import Session


class LoanWorkflowService:
    @staticmethod
    def run(loan: LoanRequest, db: Session):
        """
        Runs the loan workflow:
        1. Derive features from business/guarantor/credit
        2. Run matching against lenders
        Returns match results (without saving to DB)
        """
        feature_service = FeatureService(db_session=db)
        features = feature_service.derive_features(loan_request_id=loan.id)
        matching_service = MatchingService(db_session=db)
        matches = matching_service.match_loan(loan_request_id=loan.id)
        return matches
