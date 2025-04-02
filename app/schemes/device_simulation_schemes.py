from pydantic import BaseModel
import uuid

class DeviceSimulation(BaseModel):
    name: str
    description: str | None = None
    consumption_value: float
    is_default: bool
    peak_consumption: float | None = None
    cycle_duration: int | None = None
    on_duration: int | None = None
    electric_meter_id: uuid.UUID
    algorithm_id: uuid.UUID

class DeviceSimulationResponse(DeviceSimulation):
    id: uuid.UUID


