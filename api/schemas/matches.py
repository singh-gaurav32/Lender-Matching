from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class MatchResultOut(BaseModel):
    loan_request_id: int
    lender_id: int
    program_id: int
    eligible: bool
    fit_score: float
    summary: Optional[List[Union[Dict, str]]]

    model_config = ConfigDict(
        from_attributes=True,
    )
