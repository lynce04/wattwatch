from datetime import datetime
from pydantic import BaseModel, field_serializer

class SimulationResultBase(BaseModel):
    simulation_id: int
    real_co2: float
    simulated_co2: float
    difference: float
    percentage_change: float

class SimulationResultResponse(SimulationResultBase):
    id: int
    created_at: datetime

    @field_serializer('created_at')
    def format_created_at(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S UTC")

    class Config:
        from_attributes = True