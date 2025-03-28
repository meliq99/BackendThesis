from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class Simulation(BaseModel):
    name: str
    start_date: datetime | None = None
    update_date: datetime | None = None
    is_active: bool
    
class SimulationResponse(Simulation):
    id: UUID
    electric_meter_id: UUID | None = None