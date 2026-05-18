from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime ,timezone
from database.base import Base


class Emission(Base):
    __tablename__ = "emissions"
    id = Column(Integer, primary_key=True, index=True)
    co2_intensity = Column(Float, nullable=False)
    region = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)
    created_at =Column(DateTime, default=lambda: datetime.now(timezone.utc))