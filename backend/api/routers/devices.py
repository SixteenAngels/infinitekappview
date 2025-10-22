from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.db import get_db
from core.security import get_current_user_id
from models.device import Device
from schemas.devices import DeviceCreate, DevicePublic, DeviceUpdate

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=List[DevicePublic])
def list_devices(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    devices = db.query(Device).filter(Device.owner_id == user_id).all()
    return [DevicePublic.model_validate(d, from_attributes=True) for d in devices]


@router.post("/", response_model=DevicePublic)
def create_device(device_in: DeviceCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    device = Device(name=device_in.name, device_id=device_in.device_id, owner_id=user_id, group=device_in.group)
    db.add(device)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Device ID already exists")
    db.refresh(device)
    return DevicePublic.model_validate(device, from_attributes=True)


@router.patch("/{id}", response_model=DevicePublic)
def update_device(id: int, device_in: DeviceUpdate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    device: Optional[Device] = db.query(Device).filter(Device.id == id, Device.owner_id == user_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if device_in.name is not None:
        device.name = device_in.name
    if device_in.group is not None:
        device.group = device_in.group
    db.commit()
    db.refresh(device)
    return DevicePublic.model_validate(device, from_attributes=True)


@router.delete("/{id}")
def delete_device(id: int, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    device: Optional[Device] = db.query(Device).filter(Device.id == id, Device.owner_id == user_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"ok": True}
