from sqlmodel import Field, SQLModel, TIMESTAMP, Column, text
import uuid
from datetime import datetime


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

class ConsumptionAlgorithm(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str | None = None
    algorithm_type: str = Field(index=True)
    script: str






