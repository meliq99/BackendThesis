from pydantic import BaseModel
from uuid import UUID

class ElectricMeter(BaseModel):
   base_comsumption: float
   simulation_id: UUID

class ElectricMeterResponse(ElectricMeter):
   id: UUID