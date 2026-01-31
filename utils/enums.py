from enum import Enum, IntEnum

class FeatureType(str, Enum):
    FICO = "fico"
    PAYNET = "paynet"
    YEARS_IN_BUSINESS = "years_in_business"
    REVENUE = "revenue"
    INDUSTRY = "industry"
    STATE = "state"
    EQUIPMENT_AGE = "equipment_age"

class Operator(str, Enum):
    GTE = ">="
    LTE = "<="
    BETWEEN = "between"
    IN = "in"
    NOT_IN = "not_in"

class RuleType(str, Enum):
    FICO = "fico"
    PAYNET = "paynet"
    TIME_IN_BUSINESS = "time_in_business"
    LOAN_AMOUNT = "loan_amount"
    INDUSTRY = "industry"
    GEO = "geo"
    EQUIPMENT = "equipment"

class PolicyWeight(IntEnum):
    LOW = 1
    MEDIUM = 3
    HIGH = 5