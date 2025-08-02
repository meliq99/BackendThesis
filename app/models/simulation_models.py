from sqlmodel import Field, SQLModel, TIMESTAMP, Column, text
import uuid
from datetime import datetime
from typing import Optional


class Simulation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    start_date: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True),
                          nullable=False,
                          server_default=text("CURRENT_TIMESTAMP"))
    )
    update_date: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True),
                          nullable=False,
                          server_default=text("CURRENT_TIMESTAMP"))
    )
    is_active: bool = Field(index=True)
    output_unit: str = Field(default="W", description="Unit for frontend display (W, kW, kWh/year, kWh/month)")
    time_unit: str = Field(default="seconds", description="Time unit for algorithms (seconds, minutes, hours)")
    time_speed: float = Field(default=1.0, description="Simulation speed multiplier (1.0 = real-time)")
    simulation_start_time: Optional[datetime] = Field(default=None, description="Custom start time for simulation")

class ConsumptionAlgorithm(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str | None = None
    algorithm_type: str = Field(index=True)
    script: str






