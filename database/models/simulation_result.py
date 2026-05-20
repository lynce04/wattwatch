from datetime import datetime, timezone

from sqlalchemy import Column, DateTime,Integer,Float

from database.base import Base

class SimulationResult(Base):
     __tablename__ = "simulation_results"
     id  = Column(Integer, primary_key=True,index=True)
     simulation_id = Column(Integer, nullable=False)
     real_co2 = Column(Float)
     simulated_co2 = Column(Float)
     difference = Column(Float)
     percentage_change = Column(Float)
     created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))