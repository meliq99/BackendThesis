from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class Simulation(BaseModel):
    name: str
    start_date: datetime | None = None
    update_date: datetime | None = None
    is_active: bool
    output_unit: str = "W"  # Default to watts
    time_unit: str = Field(default="seconds", description="Time unit for algorithms (seconds, minutes, hours)")
    time_speed: float = Field(default=1.0, description="Simulation speed multiplier (1.0 = real-time)")
    simulation_start_time: Optional[datetime] = Field(default=None, description="Custom start time for simulation")
    
class SimulationResponse(Simulation):
    id: UUID
    electric_meter_id: UUID | None = None

class ConsumptionAlgorithm(BaseModel):
    name: str
    description: str | None = None
    algorithm_type: str
    script: str

class ConsumptionAlgorithmResponse(ConsumptionAlgorithm):
    id: UUID

