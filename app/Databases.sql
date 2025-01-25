from typing import Optional
from sqlmodel import Field, SQLModel;

class Medidor (SQLModel, table=True):
    id:Optional[int] = Field (default = None, primary_key=True)
    consumo_base [int] 
    consumo_total [int]

