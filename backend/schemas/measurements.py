from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MeasurementCreate(BaseModel):
    device_id: str
    sensor: str
    value: float
    unit: Optional[str] = None


class MeasurementPublic(BaseModel):
    id: int
    device_id: str
    sensor: str
    value: float
    unit: Optional[str]
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
