from database.session import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

class RuleResult(Base):
    __tablename__ = "rule_results"
    id = Column(Integer, primary_key=True, index=True)
    match_result_id = Column(Integer, ForeignKey("match_results.id"))
    rule_id = Column(Integer, ForeignKey("policy_rules.id"))
    passed = Column(Boolean, nullable=False)
    reason = Column(String)
    score_delta = Column(Float, default=0.0)

class MatchResult(Base):
    __tablename__ = "match_results"
    id = Column(Integer, primary_key=True, index=True)
    loan_request_id = Column(Integer, ForeignKey("loan_requests.id"))
    lender_id = Column(Integer, ForeignKey("lenders.id"))
    program_id = Column(Integer, ForeignKey("lender_programs.id"))
    eligible = Column(Boolean, nullable=False)
    fit_score = Column(Float, default=0.0)
    # optional summary reasons
    summary = Column(JSON)
