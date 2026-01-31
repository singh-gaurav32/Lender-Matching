from database.session import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, INTEGER, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum

class LoanStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSING = "processing"


class LoanRequest(Base):
    __tablename__ = "loan_requests"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    amount = Column(Float, nullable=False)
    status = Column(SQLEnum(LoanStatus), nullable=False, default=LoanStatus.DRAFT)
    term_months = Column(Integer, nullable=False)
    equipment_type = Column(String, nullable=False)
    equipment_year = Column(Integer, nullable=False)
    business = relationship("Business", back_populates="loans")