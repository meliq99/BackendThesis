from pydantic import BaseModel
from uuid import UUID

class Device(BaseModel):
    name: str
    description: str | None = None
    consumption_value: float
    consumption_algorithm: str
    is_default: bool

class DeviceResponse(Device):
    id: UUID