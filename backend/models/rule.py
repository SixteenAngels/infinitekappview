from sqlalchemy import Boolean, Column, Integer, String, Text

from core.db import Base


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    conditions = Column(Text, nullable=False)  # JSON string
    actions = Column(Text, nullable=False)  # JSON string
    enabled = Column(Boolean, default=True, nullable=False)
