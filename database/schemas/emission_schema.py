from datetime import datetime

from pydantic import BaseModel

class EmissionBase(BaseModel):
    region: str
    co2_intensity: float
    timestamp: int

class EmissionResponse(EmissionBase):
    id:int
    created_at:datetime

    class Config:
        from_attributes = True

