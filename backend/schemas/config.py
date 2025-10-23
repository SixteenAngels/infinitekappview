from typing import Optional

from pydantic import BaseModel

from models.device import Device


class DeviceConfig(BaseModel):
    id: int
    name: str
    group: Optional[str]

    @staticmethod
    def from_db(device: Device) -> "DeviceConfig":
        return DeviceConfig(id=device.id, name=device.name, group=device.group)


class DeviceConfigUpdate(BaseModel):
    name: Optional[str] = None
    group: Optional[str] = None
