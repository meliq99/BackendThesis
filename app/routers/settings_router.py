from fastapi import APIRouter, status, Depends
from schemes.settings_schemes import Device, DeviceResponse, Settings
from typing import Any, Annotated
from utils.get_db_connection import get_session
from services import settings_service
import uuid

router = APIRouter(
    prefix="/settings",
    tags=["settings"],
)
SessionDependency = Annotated[Any, Depends(get_session)]

@router.post("/devices", status_code=status.HTTP_201_CREATED, response_model=DeviceResponse)
async def create_device(device: Device, session: SessionDependency) -> Any:
    """
    Create a new device template in the settings.
    
    Device templates define the base configuration for devices that can be
    used in simulations, including default consumption patterns and metadata.
    
    Example request:
    ```json
    {
        "name": "Smart TV 55 inch",
        "description": "Energy-efficient LED smart television",
        "category": "entertainment",
        "default_consumption": 120,
        "peak_consumption": 180,
        "standby_consumption": 15,
        "energy_class": "A+",
        "icon": "tv",
        "manufacturer": "Samsung",
        "model": "UE55TU7020"
    }
    ```
    
    Returns:
    - Created device template with generated ID
    - All device specifications and metadata
    - Default consumption parameters
    
    Use this to:
    - Define reusable device templates
    - Set up device catalog for simulations
    - Standardize device configurations
    """
    new_device = await settings_service.create_device_service(device, session)
    return new_device
    

@router.get("/", status_code=status.HTTP_200_OK, response_model=Settings)
async def get_settings(session: SessionDependency) -> Any:
    """
    Retrieve complete system settings and configuration.
    
    Get all system-wide settings including device templates, default values,
    preferences, and configuration parameters.
    
    Returns:
    - All system settings and preferences
    - Available device templates
    - Default configuration values
    - System-wide parameters
    - User preferences and customizations
    
    Use this to:
    - Initialize application with current settings
    - Display configuration options in admin panels
    - Backup current system configuration
    - Review all available device templates
    
    📝 **Note**: This endpoint returns comprehensive system state,
    making it ideal for application initialization and admin interfaces.
    """
    return await settings_service.get_settings_service(session)

@router.delete("/devices/{device_id}", status_code=status.HTTP_200_OK)
async def delete_device(device_id: uuid.UUID, session: SessionDependency) -> Any:
    """
    Delete a device template from settings.
    
    ⚠️ **Warning**: This removes the device template permanently.
    Ensure it's not being used by any active simulations before deletion.
    
    Path Parameters:
    - **device_id**: UUID of the device template to delete
    
    Returns:
    - Success confirmation message
    
    Raises:
    - 404: Device template not found
    - 400: Device is in use by simulations (if validation implemented)
    - 400: Invalid UUID format
    
    Before deletion:
    - Check if device template is used in any simulations
    - Export device configuration for backup
    - Verify this is the correct template to remove
    
    📝 **Note**: This only removes the template, not actual device
    simulations that may be using this template.
    """
    return await settings_service.delete_device_service(device_id, session)
    
@router.put("/devices/{device_id}", status_code=status.HTTP_200_OK, response_model=DeviceResponse)
async def update_device(device_id: uuid.UUID, device: Device, session: SessionDependency) -> Any:
    """
    Update an existing device template in settings.
    
    Modify device template parameters, consumption values, or metadata.
    Changes will apply to new simulations using this template.
    
    Path Parameters:
    - **device_id**: UUID of the device template to update
    
    Example request (updating consumption values):
    ```json
    {
        "name": "Smart TV 55 inch - Updated",
        "description": "Ultra energy-efficient QLED smart television",
        "default_consumption": 100,
        "peak_consumption": 150,
        "standby_consumption": 12,
        "energy_class": "A++"
    }
    ```
    
    Returns:
    - Updated device template with all current values
    - New modification timestamp
    
    Raises:
    - 404: Device template not found
    - 400: Invalid update data or UUID format
    
    📝 **Note**: Updates to templates don't affect existing device
    simulations; they only apply to new simulations created after the update.
    """
    return await settings_service.update_device_service(device_id, device, session)