from datetime import datetime

from pydantic import BaseModel

class SimulationBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    scenario:str

class SimulationResponse(SimulationBase):
    id:int
    created_at:datetime

    class Config:
        from_attributes = True