from sqlmodel import Field, SQLModel, TIMESTAMP, Column, text
import uuid
from typing import Optional

class DeviceSimulation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    consumption_value: float 
    is_default: bool = Field(index=True)
    peak_consumption: Optional[float] = None
    cycle_duration: Optional[int] = None
    on_duration: Optional[int] = None
    algorithm_id: uuid.UUID = Field(default=None, foreign_key="consumptionalgorithm.id")
    electric_meter_id: uuid.UUID = Field(default=None, foreign_key="electricmeter.id")




