from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.db import get_db
from core.security import get_current_user_id
from models.device import Device
from schemas.config import DeviceConfig, DeviceConfigUpdate

router = APIRouter(prefix="/devices", tags=["config"])  # share namespace under /devices


@router.get("/{id}/config", response_model=DeviceConfig)
def get_config(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    device = db.query(Device).filter(Device.id == id, Device.owner_id == user_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return DeviceConfig.from_db(device)


@router.put("/{id}/config", response_model=DeviceConfig)
def put_config(
    id: int,
    config_in: DeviceConfigUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    device = db.query(Device).filter(Device.id == id, Device.owner_id == user_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    device.name = config_in.name if config_in.name is not None else device.name
    device.group = config_in.group if config_in.group is not None else device.group
    db.commit()
    db.refresh(device)
    return DeviceConfig.from_db(device)
