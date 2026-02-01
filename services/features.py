from datetime import date
from utils.enums import FeatureType
from models import LoanRequest, BusinessFeature

FEATURE_SOURCES = {
    FeatureType.FICO: lambda b, l: b.guarantor.fico_score if b.guarantor else None,
    FeatureType.PAYNET: lambda b, l: b.credit.paynet_score if b.credit else None,
    FeatureType.YEARS_IN_BUSINESS: lambda b, l: b.years_in_business,
    FeatureType.REVENUE: lambda b, l: b.annual_revenue,
    FeatureType.INDUSTRY: lambda b, l: b.industry,
    FeatureType.STATE: lambda b, l: b.state,
    FeatureType.EQUIPMENT_AGE: lambda b, l: date.today().year - l.equipment_year,
}


class FeatureService:
    def __init__(self, db_session):
        self.db = db_session

    def derive_features(self, loan_request_id: int):
        loan = self.db.get(LoanRequest, loan_request_id)
        business = loan.business

        features = []
        for ft, func in FEATURE_SOURCES.items():
            val = func(business, loan)
            if val is not None:
                features.append(
                    BusinessFeature(business_id=business.id, feature_type=ft, value=val)
                )
                self.db.add(features[-1])

        self.db.commit()
        return features
