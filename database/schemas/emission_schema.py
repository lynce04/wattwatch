from datetime import datetime,timezone,timedelta

from pydantic import BaseModel,field_serializer

class EmissionBase(BaseModel):
    region: str
    co2_intensity: float
    timestamp: int

class EmissionResponse(EmissionBase):
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def format_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S UTC")

    class Config:
        from_attributes = True