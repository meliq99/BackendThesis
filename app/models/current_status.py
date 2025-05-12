from sqlmodel import Field, SQLModel, TIMESTAMP
import uuid
from typing import Optional

class CurrentStatus(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str = Field(index=True, nullable=False)