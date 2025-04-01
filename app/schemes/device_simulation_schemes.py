from pydantic import BaseModel
import uuid

class DeviceSimulation(BaseModel):
    name: str
    description: str | None = None
    consumption_value: float
    consumption_algorithm: str
    is_default: bool
    electric_meter_id: uuid.UUID

class DeviceSimulationResponse(DeviceSimulation):
    id: uuid.UUID


