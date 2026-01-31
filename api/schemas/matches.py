from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
# -----------------------------
# Match Result
# -----------------------------
class MatchResultOut(BaseModel):
    lender_id: int
    program_id: int
    eligible: bool
    fit_score: float
    summary: Optional[List[Dict]]  # reasons per rule

    model_config = ConfigDict(
        from_attributes=True,
        # ... other config options ...
    )
