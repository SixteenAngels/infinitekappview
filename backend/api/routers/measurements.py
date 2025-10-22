from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.db import get_db
from core.security import get_current_user_id
from models.measurement import Measurement
from schemas.measurements import MeasurementCreate, MeasurementPublic

router = APIRouter(prefix="/measurements", tags=["measurements"])


@router.post("/", response_model=MeasurementPublic)
def ingest(measurement_in: MeasurementCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    measurement = Measurement(
        device_id=measurement_in.device_id,
        sensor=measurement_in.sensor,
        value=measurement_in.value,
        unit=measurement_in.unit,
        created_at=datetime.utcnow(),
        owner_id=user_id,
    )
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return MeasurementPublic.model_validate(measurement, from_attributes=True)


@router.get("/", response_model=List[MeasurementPublic])
def list_measurements(
    device_id: Optional[str] = None,
    sensor: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    q = db.query(Measurement).filter(Measurement.owner_id == user_id)
    if device_id:
        q = q.filter(Measurement.device_id == device_id)
    if sensor:
        q = q.filter(Measurement.sensor == sensor)
    q = q.order_by(Measurement.created_at.desc()).limit(limit)
    items = q.all()
    return [MeasurementPublic.model_validate(m, from_attributes=True) for m in items]
