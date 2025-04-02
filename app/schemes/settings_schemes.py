from pydantic import BaseModel
from uuid import UUID
from schemes.simulation_schemes import SimulationResponse, ConsumptionAlgorithmResponse

class Device(BaseModel):
    name: str
    description: str | None = None
    consumption_value: float
    is_default: bool
    peak_consumption: float | None = None
    cycle_duration: int | None = None
    on_duration: int | None = None
    algorithm_id: UUID

class DeviceResponse(Device):
    id: UUID

class Settings(BaseModel):
    devices: list[DeviceResponse] = []
    simulation: SimulationResponse
    consumption_algorithms: list[ConsumptionAlgorithmResponse] = []
