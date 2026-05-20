from datetime import datetime

from pydantic import BaseModel,field_serializer



class SimulationBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    scenario:str

class SimulationResponse(SimulationBase):
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def format_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S UTC")

    class Config:
        from_attributes = True