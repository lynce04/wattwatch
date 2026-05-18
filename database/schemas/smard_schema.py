from datetime import datetime
from pydantic import BaseModel

class SmardDataBase(BaseModel):
    filter_id :int
    region:str
    timestamp:int
    value:float

class SmardDataResponse(SmardDataBase):
     id: int
     created_at: datetime

     class Config:
         from_attributes = True
