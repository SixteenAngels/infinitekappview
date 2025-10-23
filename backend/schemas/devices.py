from typing import Optional

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    name: str
    device_id: str
    group: Optional[str] = None


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    group: Optional[str] = None


class DevicePublic(BaseModel):
    id: int
    name: str
    device_id: str
    group: Optional[str]

    model_config = {
        "from_attributes": True,
    }
