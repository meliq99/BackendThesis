from fastapi import APIRouter, status, Depends, HTTPException
from schemes.simulation_schemes import Simulation, SimulationResponse, SimulationUpdate
from typing import Any, Annotated
from utils.get_db_connection import get_session
from services.simulation_service import create_simulation_service, update_simulation_service, get_active_simulation_service
import uuid

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

@router.get("/active", response_model=SimulationResponse)
async def get_active_simulation(session: SessionDependency) -> Any:
    """
    Get the currently active simulation with all parameters.
    
    Returns the simulation that is currently being used for real-time
    energy consumption calculations and data generation.
    
    Returns:
    - Active simulation configuration
    - All timing and unit parameters
    - Current simulation state
    
    Use this to:
    - Check current simulation settings
    - Display simulation parameters in UI
    - Verify configuration before updates
    """
    active_simulation = await get_active_simulation_service(session)
    if not active_simulation:
        raise HTTPException(status_code=404, detail="No active simulation found")
    return active_simulation

@router.put("/{simulation_id}", response_model=SimulationResponse)
async def update_simulation_parameters(
    simulation_id: uuid.UUID,
    simulation_update: SimulationUpdate,
    session: SessionDependency
) -> Any:
    """
    Update simulation parameters including time and unit settings.
    
    Update specific parameters of a simulation without affecting others.
    Changes take effect immediately for real-time consumption calculations.
    
    Example requests:
    
    **Update output unit only:**
    ```json
    {
        "output_unit": "kW"
    }
    ```
    
    **Update time settings:**
    ```json
    {
        "time_unit": "minutes",
        "time_speed": 60.0,
        "simulation_start_time": "2024-01-01T00:00:00Z"
    }
    ```
    
    **Update multiple parameters:**
    ```json
    {
        "name": "Updated Home Energy Analysis",
        "output_unit": "kWh/day",
        "time_unit": "hours",
        "time_speed": 24.0,
        "simulation_start_time": "2024-01-01T06:00:00Z"
    }
    ```
    
    Returns:
    - Updated simulation with all current parameters
    - Immediate effect on real-time calculations
    
    ⚡ **Real-time Impact**: Changes are applied immediately to:
    - MQTT data publishing units
    - Time progression calculations
    - Algorithm time parameters
    
    💡 **Pro Tips**:
    - Use `time_speed > 1` for accelerated simulations
    - Use `time_speed < 1` for slow-motion analysis
    - Set `simulation_start_time` for historical replays
    """
    updated_simulation = await update_simulation_service(simulation_id, simulation_update, session)
    if not updated_simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return updated_simulation

@router.put("/active/parameters", response_model=SimulationResponse)
async def update_active_simulation_parameters(
    simulation_update: SimulationUpdate,
    session: SessionDependency
) -> Any:
    """
    Update parameters of the currently active simulation.
    
    Convenient endpoint to update the active simulation without needing
    to specify the simulation ID. Perfect for quick parameter adjustments.
    
    Example requests:
    
    **Quick unit change:**
    ```json
    {
        "output_unit": "kWh/year"
    }
    ```
    
    **Speed up simulation 10x:**
    ```json
    {
        "time_speed": 10.0
    }
    ```
    
    **Change time unit to minutes:**
    ```json
    {
        "time_unit": "minutes"
    }
    ```
    
    Returns:
    - Updated active simulation
    - Immediate effect on real-time data
    
    🎯 **Use Cases**:
    - Quick testing of different units
    - Real-time simulation speed adjustments
    - Live parameter tuning during demonstrations
    """
    # Get active simulation first
    active_simulation = await get_active_simulation_service(session)
    if not active_simulation:
        raise HTTPException(status_code=404, detail="No active simulation found")
    
    # Update it
    updated_simulation = await update_simulation_service(
        active_simulation["id"], 
        simulation_update, 
        session
    )
    if not updated_simulation:
        raise HTTPException(status_code=500, detail="Failed to update simulation")
    
    return updated_simulation

@router.get("/supported-options")
async def get_supported_simulation_options() -> Any:
    """
    Get supported options for simulation parameters.
    
    Returns available values for output units, time units, and 
    recommendations for time speeds and simulation configurations.
    
    Returns:
    - Supported output units with descriptions
    - Supported time units with multipliers
    - Time speed recommendations
    - Configuration examples
    
    Use this to:
    - Populate frontend dropdowns
    - Validate parameter values
    - Show configuration options to users
    """
    return {
        "output_units": {
            "W": {
                "description": "Watts (instantaneous power)",
                "use_case": "Real-time power monitoring"
            },
            "kW": {
                "description": "Kilowatts (instantaneous power)",
                "use_case": "High-power devices and systems"
            },
            "kWh/day": {
                "description": "Kilowatt-hours per day (daily energy)",
                "use_case": "Daily energy consumption analysis"
            },
            "kWh/month": {
                "description": "Kilowatt-hours per month (monthly energy)",
                "use_case": "Monthly billing and planning"
            },
            "kWh/year": {
                "description": "Kilowatt-hours per year (annual energy)",
                "use_case": "Annual energy efficiency analysis"
            }
        },
        "time_units": {
            "seconds": {
                "description": "Seconds (default)",
                "multiplier": 1,
                "use_case": "Fine-grained analysis"
            },
            "minutes": {
                "description": "Minutes",
                "multiplier": 60,
                "use_case": "Medium-term patterns"
            },
            "hours": {
                "description": "Hours",
                "multiplier": 3600,
                "use_case": "Daily patterns and cycles"
            }
        },
        "time_speed_recommendations": {
            "real_time": {
                "value": 1.0,
                "description": "Real-time simulation (1:1 ratio)"
            },
            "fast_preview": {
                "value": 60.0,
                "description": "1 minute = 1 hour (fast preview)"
            },
            "daily_in_minutes": {
                "value": 1440.0,
                "description": "1 minute = 1 day (daily overview)"
            },
            "slow_analysis": {
                "value": 0.1,
                "description": "10 seconds = 1 second (detailed analysis)"
            }
        },
        "configuration_examples": [
            {
                "name": "Real-time Monitoring",
                "output_unit": "W",
                "time_unit": "seconds",
                "time_speed": 1.0,
                "description": "Live power consumption monitoring"
            },
            {
                "name": "Daily Energy Analysis",
                "output_unit": "kWh/day",
                "time_unit": "hours",
                "time_speed": 24.0,
                "description": "Analyze daily energy patterns in real-time"
            },
            {
                "name": "Fast Testing",
                "output_unit": "kW",
                "time_unit": "minutes",
                "time_speed": 60.0,
                "description": "Quick simulation testing and development"
            },
            {
                "name": "Historical Replay",
                "output_unit": "W",
                "time_unit": "seconds",
                "time_speed": 3600.0,
                "simulation_start_time": "2024-01-01T00:00:00Z",
                "description": "Replay historical data at high speed"
            }
        ]
    }

