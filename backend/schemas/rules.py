from typing import Any, Dict, Optional

from pydantic import BaseModel


class RuleCreate(BaseModel):
    name: str
    conditions: str  # JSON string for now
    actions: str  # JSON string for now


class RuleUpdate(BaseModel):
    name: Optional[str] = None
    conditions: Optional[str] = None
    actions: Optional[str] = None
    enabled: Optional[bool] = None


class RulePublic(BaseModel):
    id: int
    owner_id: str
    name: str
    conditions: str
    actions: str
    enabled: bool

    model_config = {
        "from_attributes": True,
    }
