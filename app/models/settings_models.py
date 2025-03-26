from sqlmodel import Field,  SQLModel
import uuid

class Device(SQLModel, table=True): 
    id: uuid.UUID  = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)    
    description: str | None = None 
    consumption_value: float
    consumption_algorithm: str
    is_default: bool = Field(index=True)
    
