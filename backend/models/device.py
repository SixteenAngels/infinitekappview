from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint

from core.db import Base


class Device(Base):
    __tablename__ = "devices"
    __table_args__ = (UniqueConstraint("device_id", name="uq_device_id"),)

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    group = Column(String, nullable=True)
    owner_id = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
