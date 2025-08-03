from pydantic import BaseModel
from typing import Optional

# Define a data model using Pydantic MODELS
class DataModel(BaseModel):
    value: float
    unit: Optional[str] = None
    time_unit: Optional[str] = None
    time_speed: Optional[float] = None
    simulation_id: Optional[str] = None
    timestamp: Optional[int] = None
