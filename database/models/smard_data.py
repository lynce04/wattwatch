from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime,timezone


from database.base import Base


class SmardData(Base):
    __tablename__ = "smard_data"

    id = Column(Integer, primary_key=True, index=True)

    filter_id = Column(Integer, nullable=False)

    region =  Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)
    value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))