from sqlmodel import Field, SQLModel, TIMESTAMP, Column, text
import uuid
from datetime import datetime

class DeviceSimulation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    consumption_value: float 
    consumption_algorithm: str 
    is_default: bool = Field(index=True)
    electric_meter_id: uuid.UUID = Field(default=None, foreign_key="electricmeter.id")




