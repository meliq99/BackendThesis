from pydantic import BaseModel
from uuid import UUID
from schemes.simulation_schemes import SimulationResponse

class Device(BaseModel):
    name: str
    description: str | None = None
    consumption_value: float
    consumption_algorithm: str
    is_default: bool

class DeviceResponse(Device):
    id: UUID

class Settings(BaseModel):
    devices: list[DeviceResponse] = []
    simulation: SimulationResponse
