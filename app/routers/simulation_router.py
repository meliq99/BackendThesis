from fastapi import APIRouter, status, Depends
from schemes.simulation_schemes import Simulation, SimulationResponse
from typing import Any, Annotated
from utils.get_db_connection import get_session
from services.simulation_service import create_simulation_service

router = APIRouter(
    prefix="/simulations",
    tags=["simulations"],
)

SessionDependency = Annotated[Any, Depends(get_session)]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=SimulationResponse)
async def create_simulation(simulation: Simulation, session: SessionDependency) -> Any:
    new_simulation = await create_simulation_service(simulation, session)
    return new_simulation
