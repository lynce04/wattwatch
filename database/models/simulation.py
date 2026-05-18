from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime,timezone

from database.base import Base


class Simulations(Base):
    __tablename__ = "simulations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    scenario = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at =Column(DateTime, default=lambda: datetime.now(timezone.utc))