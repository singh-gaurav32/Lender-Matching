from database.session import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from utils.enums import PolicyWeight


class Lender(Base):
    __tablename__ = "lenders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    programs = relationship("LenderProgram", back_populates="lender")


class LenderProgram(Base):
    __tablename__ = "lender_programs"
    id = Column(Integer, primary_key=True, index=True)
    lender_id = Column(Integer, ForeignKey("lenders.id"))
    name = Column(String, nullable=False)
    rules = relationship("PolicyRule", back_populates="program")
    lender = relationship("Lender", back_populates="programs")



class PolicyRule(Base):
    __tablename__ = "policy_rules"
    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("lender_programs.id"))
    rule_type = Column(String, nullable=False)
    operator = Column(String, nullable=False)
    is_hard = Column(Boolean, default=False)
    value = Column(JSON, nullable=False)
    weight = Column(Integer, default=PolicyWeight.MEDIUM)
    program = relationship("LenderProgram", back_populates="rules")