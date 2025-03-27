from sqlmodel import Field, SQLModel
import uuid


class ElectricMeter(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    base_comsumption: float 
    simulation_id: uuid.UUID = Field(default=None, foreign_key="simulation.id")
    