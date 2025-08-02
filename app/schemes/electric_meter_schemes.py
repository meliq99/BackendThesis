from pydantic import BaseModel, Field
from uuid import UUID

class ElectricMeter(BaseModel):
   base_consumption: float = Field(description="Base power consumption in watts (W)")
   simulation_id: UUID

class ElectricMeterResponse(ElectricMeter):
   id: UUID