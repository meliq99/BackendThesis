from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from typing import Annotated, Any, Dict
from utils.get_db_connection import get_session
from utils.publisher import publish_messages, publish_message
from services import publisher_service
import asyncio
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/publisher",
    tags=["publisher"],
)

# Will be assigned in main.py
mqtt_service = None
publish_task = None

SessionDependency = Annotated[Any, Depends(get_session)]

@router.post("/{simulation_id}/start", status_code=status.HTTP_200_OK)
async def start_publisher(simulation_id: uuid.UUID, background_tasks: BackgroundTasks, session: SessionDependency) -> Dict[str, str]:
    """
    Start the MQTT publisher for real-time data streaming.
    
    Initiates background publishing of simulation data to MQTT broker,
    enabling real-time monitoring and data streaming for the specified simulation.
    
    Path Parameters:
    - **simulation_id**: UUID of the simulation to start publishing for
    
    Returns:
    - Status confirmation and publisher state
    
    Example response:
    ```json
    {
        "status": "Publisher started"
    }
    ```
    
    Behavior:
    - Starts background task for continuous data publishing
    - Sends status message to MQTT broker
    - Updates simulation status to "running"
    - Enables real-time data streaming
    
    Raises:
    - 500: MQTT service not initialized
    - 400: Invalid simulation ID
    
    📝 **Note**: If publisher is already running, returns current status
    without starting a new instance.
    """
    global publish_task
    
    if publish_task and not publish_task.done():
        return {"status": "Publisher already running"}
    
    if mqtt_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MQTT service not initialized"
        )
    
    publish_task = asyncio.create_task(publish_messages(mqtt_service, session))
    await publish_message(mqtt_service, {"subject": "status", "value": "started"})
    await publisher_service.save_status_service(simulation_id, "running", session)
    logger.info("Background publish task started")
    
    return {"status": "Publisher started"}

@router.post("/{simulation_id}/stop", status_code=status.HTTP_200_OK)
async def stop_publisher(simulation_id: uuid.UUID, session: SessionDependency) -> Dict[str, str]:
    """
    Stop the MQTT publisher and halt data streaming.
    
    Gracefully stops the background publishing task, ending real-time
    data streaming for the specified simulation.
    
    Path Parameters:
    - **simulation_id**: UUID of the simulation to stop publishing for
    
    Returns:
    - Status confirmation and final publisher state
    
    Example response:
    ```json
    {
        "status": "Publisher stopped"
    }
    ```
    
    Behavior:
    - Cancels background publishing task
    - Sends stop status message to MQTT broker
    - Updates simulation status to "stopped"
    - Cleanly terminates data streaming
    
    Raises:
    - 400: Invalid simulation ID
    
    📝 **Note**: If publisher is not running, returns current status
    without attempting to stop a non-existent task.
    
    ℹ️ **Safety**: This operation is graceful and ensures proper cleanup
    of resources and MQTT connections.
    """
    global publish_task
    
    if not publish_task or publish_task.done():
        return {"status": "Publisher not running"}
    
    publish_task.cancel()
    try:
        await publish_task
        logger.info("Background publish task cancelled successfully")
    except asyncio.CancelledError:
        logger.info("Background publish task has been cancelled")
    
    await publish_message(mqtt_service, {"subject": "status", "value": "stopped"})
    await publisher_service.save_status_service(simulation_id, "stopped", session)
    return {"status": "Publisher stopped"} 
