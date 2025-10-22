from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Index

from core.db import Base


class Measurement(Base):
    __tablename__ = "measurements"
    __table_args__ = (
        Index("ix_measurements_owner_device_time", "owner_id", "device_id", "created_at"),
        Index("ix_measurements_sensor_time", "sensor", "created_at"),
    )

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, nullable=False)
    sensor = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    owner_id = Column(String, index=True, nullable=False)
