from models import LoanRequest, LenderProgram, MatchResult, RuleResult
from utils.enums import FeatureType, LoanStatus


class MatchingService:
    def __init__(self, db_session):
        self.db = db_session

    def match_loan(self, loan_request_id: int):
        loan: LoanRequest = self.db.get(LoanRequest, loan_request_id)
        loan.status = LoanStatus.PROCESSING
        self.db.commit()
        business = loan.business
        programs = self.db.query(LenderProgram).all()
        results = []
        for program in programs:
            match_result = MatchResult(
                loan_request_id=loan.id,
                lender_id=program.lender_id,
                program_id=program.id,
                eligible=True,
                fit_score=0.0,
                summary=[],
            )
            self.db.add(match_result)
            fit_score = 0
            for rule in program.rules:
                feature = self._get_feature(business, rule.rule_type)
                if rule.is_hard:
                    passed, score_delta, reason = False, 0, f"{feature.val} not allowed"
                else:
                    passed, score_delta, reason = self._evaluate_rule(
                        rule, feature, loan
                    )
                # record rule result
                rule_result = RuleResult(
                    match_result_id=match_result.id,
                    rule_id=rule.id,
                    passed=passed,
                    reason=reason,
                    score_delta=score_delta,
                )
                self.db.add(rule_result)

                if not passed:
                    match_result.eligible = False
                    match_result.summary.append(reason)
                fit_score += score_delta
            match_result.fit_score = (fit_score / (len(program.rules) * 5)) * 100
            results.append(match_result)

        self.db.commit()
        loan.status = LoanStatus.COMPLETED
        self.db.commit()
        return results

    def _get_feature(self, business, rule_type: str):
        # map RuleType → FeatureType if needed
        mapping = {
            "fico": FeatureType.FICO,
            "paynet": FeatureType.PAYNET,
            "time_in_business": FeatureType.YEARS_IN_BUSINESS,
            "loan_amount": "loan_amount",
            "industry": FeatureType.INDUSTRY,
            "geo": FeatureType.STATE,
            "equipment": FeatureType.EQUIPMENT_AGE,
        }
        ft = mapping.get(rule_type)
        if ft in [
            FeatureType.FICO,
            FeatureType.PAYNET,
            FeatureType.YEARS_IN_BUSINESS,
            FeatureType.REVENUE,
            FeatureType.INDUSTRY,
            FeatureType.STATE,
            FeatureType.EQUIPMENT_AGE,
        ]:
            return next((f for f in business.features if f.feature_type == ft), None)
        return None

    def _evaluate_rule(self, rule, feature, loan_request):
        val = feature.value if feature else None
        op = rule.operator
        target = rule.value
        passed = True
        reason = ""
        score_delta = rule.weight

        if val is None:
            passed = False
            reason = f"{rule.rule_type} feature missing"
        elif op == ">=" and val < target:
            passed = False
            reason = f"{rule.rule_type} {val} < {target}"
        elif op == "<=" and val > target:
            passed = False
            reason = f"{rule.rule_type} {val} > {target}"
        elif op == "in" and val not in target:
            passed = False
            reason = f"{rule.rule_type} {val} not in {target}"
        elif op == "not_in" and val in target:
            passed = False
            reason = f"{rule.rule_type} {val} in {target}"

        return passed, score_delta if passed else 0, reason
