from fastapi import APIRouter, HTTPException, Depends
from models.data_model import DataModel
from typing import Any, Annotated
from utils.get_db_connection import get_session
from utils.publisher import get_current_simulation, calculate_simulation_time
from utils.unit_converter import watts_to_unit

router = APIRouter()
SessionDependency = Annotated[Any, Depends(get_session)]

# Assume that mqtt_service is set up and passed to the router via dependency injection or global state.
mqtt_service = None  # You can set this in your main startup event

# @router.post("/send-data/")
# async def send_data(data: DataModel):
#     if not mqtt_service:
#         raise HTTPException(status_code=500, detail="MQTT client not initialized.")
#     try:
#         message = data.dict()
#         mqtt_service.publish(message)
#         return {"status": "Message sent to MQTT Broker", "data": message}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")

@router.get("/current-parameters")
async def get_current_simulation_parameters(session: SessionDependency) -> Any:
    """
    Get current simulation parameters being used for MQTT publishing.
    
    Returns the same parameter information that is sent via MQTT,
    useful for REST API clients or initial frontend setup.
    
    Returns:
    - Current output unit for consumption values
    - Time unit and speed configuration
    - Active simulation ID
    - Current simulation timestamp
    
    Use this to:
    - Initialize frontend with current settings
    - Verify parameter changes
    - Display current simulation configuration
    """
    try:
        current_simulation = await get_current_simulation(session)
        if not current_simulation:
            raise HTTPException(status_code=404, detail="No active simulation found")
        
        simulation_time = calculate_simulation_time(current_simulation)
        
        return {
            "simulation_id": str(current_simulation.id),
            "simulation_name": current_simulation.name,
            "output_unit": current_simulation.output_unit,
            "time_unit": current_simulation.time_unit,
            "time_speed": current_simulation.time_speed,
            "simulation_start_time": current_simulation.simulation_start_time.isoformat() if current_simulation.simulation_start_time else None,
            "current_simulation_time": simulation_time,
            "is_active": current_simulation.is_active,
            "parameters_description": {
                "output_unit": f"All consumption values are published in {current_simulation.output_unit}",
                "time_unit": f"Algorithm time intervals are in {current_simulation.time_unit}",
                "time_speed": f"Simulation runs at {current_simulation.time_speed}x real-time speed",
                "effect": "These parameters affect both MQTT publishing and REST API responses"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get simulation parameters: {e}")

@router.get("/sample-mqtt-message")
async def get_sample_mqtt_message(session: SessionDependency) -> Any:
    """
    Get a sample of what the MQTT message structure looks like.
    
    Returns the current DataModel structure with example values,
    showing exactly what the frontend will receive via MQTT.
    
    Returns:
    - Sample MQTT message structure
    - Current parameter values
    - Field descriptions
    
    Use this to:
    - Understand MQTT message format
    - Test frontend MQTT parsing
    - Debug data structure issues
    """
    try:
        current_simulation = await get_current_simulation(session)
        if not current_simulation:
            raise HTTPException(status_code=404, detail="No active simulation found")
        
        simulation_time = calculate_simulation_time(current_simulation)
        
        # Create sample data with example consumption value
        sample_data = DataModel(
            value=42.5,  # Example consumption value
            unit=current_simulation.output_unit,
            time_unit=current_simulation.time_unit,
            time_speed=current_simulation.time_speed,
            simulation_id=str(current_simulation.id),
            timestamp=simulation_time
        )
        
        return {
            "mqtt_message_structure": sample_data.dict(),
            "field_descriptions": {
                "value": "Current consumption value in the specified unit",
                "unit": "Unit of measurement for the consumption value",
                "time_unit": "Time unit used by simulation algorithms",
                "time_speed": "Speed multiplier for simulation time progression",
                "simulation_id": "ID of the active simulation",
                "timestamp": "Current simulation time as Unix timestamp"
            },
            "real_time_info": {
                "message_interval": "Messages are published every 2 seconds",
                "value_updates": "Consumption value changes based on device algorithms",
                "parameter_updates": "Unit and time parameters update immediately when changed via API"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate sample message: {e}")