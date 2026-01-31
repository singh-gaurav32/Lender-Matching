from database.session import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from utils.enums import FeatureType



class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    state = Column(String, nullable=False)
    years_in_business = Column(Integer, nullable=False)
    annual_revenue = Column(Float, nullable=False)

    # relationships
    guarantor = relationship("PersonalGuarantor", back_populates="business", uselist=False)
    credit = relationship("BusinessCredit", back_populates="business", uselist=False)
    features = relationship("BusinessFeature", back_populates="business")
    loans = relationship("LoanRequest", back_populates="business")

class PersonalGuarantor(Base):
    __tablename__ = "personal_guarantors"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    fico_score = Column(Integer, nullable=False)
    has_bankruptcy = Column(Boolean, default=False)
    has_tax_liens = Column(Boolean, default=False)

    business = relationship("Business", back_populates="guarantor")

class BusinessCredit(Base):
    __tablename__ = "business_credits"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    paynet_score = Column(Float, nullable=False)
    trade_line_count = Column(Integer, default=0)

    business = relationship("Business", back_populates="credit")

class BusinessFeature(Base):
    __tablename__ = "business_features"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    feature_type = Column(SQLEnum(FeatureType), nullable=False)
    value = Column(JSON, nullable=False)

    business = relationship("Business", back_populates="features")