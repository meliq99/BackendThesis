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
    """
    Create a new energy consumption simulation.
    
    Set up a complete simulation environment with time configuration,
    units, and speed parameters for energy consumption analysis.
    
    Example request:
    ```json
    {
        "name": "Home Energy Analysis",
        "description": "24-hour household consumption simulation",
        "time_unit": "minutes",
        "time_speed": 60.0,
        "output_unit": "kWh/day",
        "simulation_duration_hours": 24.0,
        "sample_interval_seconds": 3600,
        "is_active": true,
        "auto_start": false,
        "configuration": {
            "include_weather_effects": true,
            "randomize_consumption": true,
            "base_temperature": 20.0
        }
    }
    ```
    
    Returns:
    - Created simulation with generated ID
    - All timing and configuration parameters
    - Ready for device assignment and execution
    
    Use this to:
    - Set up new energy analysis scenarios
    - Configure simulation parameters and timing
    - Prepare environment for device simulations
    
    📝 **Next Steps**: After creation, add devices and start publisher
    for real-time data generation.
    """
    new_simulation = await create_simulation_service(simulation, session)
    return new_simulation

