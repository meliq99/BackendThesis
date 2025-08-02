from fastapi import APIRouter, status, Depends
from schemes.device_simulation_schemes import DeviceSimulation, DeviceSimulationResponse
from typing import Any, Annotated
from utils.get_db_connection import get_session
from services import device_simulation_service
import uuid

router = APIRouter(
    prefix="/device-simulation",
    tags=["device-simulation"],
)
SessionDependency = Annotated[Any, Depends(get_session)]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DeviceSimulationResponse)
async def create_device_simulation(device_simulation: DeviceSimulation, session: SessionDependency) -> Any:
    """
    Create a new device simulation configuration.
    
    Device simulations define how virtual devices behave within an electric meter,
    including their consumption patterns, algorithms, and operational parameters.
    
    Example request:
    ```json
    {
        "device_name": "Kitchen Refrigerator",
        "algorithm_id": "550e8400-e29b-41d4-a716-446655440000",
        "electric_meter_id": "550e8400-e29b-41d4-a716-446655440001",
        "base_consumption": 150,
        "peak_consumption": 300,
        "is_active": true,
        "schedule": {
            "start_time": "00:00",
            "end_time": "23:59",
            "days_of_week": [1,2,3,4,5,6,7]
        }
    }
    ```
    
    Returns:
    - Created device simulation with generated ID
    - All configuration parameters
    - Associated algorithm and meter information
    """
    new_device_simulation = await device_simulation_service.create_device_simulation_service(device_simulation, session)
    return new_device_simulation

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[DeviceSimulationResponse])
async def get_device_simulations(electric_meter_id: uuid.UUID, session: SessionDependency) -> Any:
    """
    Retrieve all device simulations for a specific electric meter.
    
    Get a comprehensive list of all devices configured within a particular
    electric meter, including their current status and configurations.
    
    Query Parameters:
    - **electric_meter_id**: UUID of the electric meter to get devices for
    
    Returns:
    - List of all device simulations for the specified meter
    - Device configurations and current status
    - Associated algorithm information
    - Consumption parameters and schedules
    
    Use this to:
    - Display all devices in a meter's dashboard
    - Monitor device simulation status
    - Review device configurations
    """
    return await device_simulation_service.get_device_simulations_service(electric_meter_id, session)

@router.delete("/{device_simulation_id}", status_code=status.HTTP_200_OK)
async def delete_device_simulation(device_simulation_id: uuid.UUID, session: SessionDependency) -> Any:
    """
    Delete a device simulation from the system.
    
    ⚠️ **Warning**: This permanently removes the device simulation
    and all its historical data. This action cannot be undone.
    
    Path Parameters:
    - **device_simulation_id**: UUID of the device simulation to delete
    
    Returns:
    - Success confirmation message
    
    Raises:
    - 404: Device simulation not found
    - 400: Invalid UUID format
    
    Before deletion:
    - Stop any running simulations using this device
    - Export historical data if needed for analysis
    - Verify this is the correct device to remove
    """
    return await device_simulation_service.delete_device_simulation_service(device_simulation_id, session)

@router.put("/{device_simulation_id}", status_code=status.HTTP_200_OK, response_model=DeviceSimulationResponse)
async def update_device_simulation(device_simulation_id: uuid.UUID, device_simulation: DeviceSimulation, session: SessionDependency) -> Any:
    """
    Update an existing device simulation configuration.
    
    Modify device parameters, consumption values, schedules, or algorithm assignments.
    Changes take effect immediately for running simulations.
    
    Path Parameters:
    - **device_simulation_id**: UUID of the device simulation to update
    
    Example request (updating consumption and schedule):
    ```json
    {
        "device_name": "Kitchen Refrigerator - Updated",
        "base_consumption": 140,
        "peak_consumption": 280,
        "is_active": true,
        "schedule": {
            "start_time": "06:00",
            "end_time": "22:00",
            "days_of_week": [1,2,3,4,5]
        }
    }
    ```
    
    Returns:
    - Updated device simulation with all current values
    - New modification timestamp
    
    Raises:
    - 404: Device simulation not found
    - 400: Invalid update data or UUID format
    
    📝 **Note**: Updates to active simulations may cause temporary
    fluctuations in consumption patterns as new parameters take effect.
    """
    return await device_simulation_service.update_device_simulation_service(device_simulation_id, device_simulation, session)
