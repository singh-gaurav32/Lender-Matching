from app.models import LoanRequest
from app.features import derive_features
from app.matching import run_matching

class LoanWorkflowService:
    @staticmethod
    def run(loan: LoanRequest):
        """
        Runs the loan workflow:
        1. Derive features from business/guarantor/credit
        2. Run matching against lenders
        Returns match results (without saving to DB)
        """
        features = derive_features(loan.business)
        matches = run_matching(loan, features)
        return matches
