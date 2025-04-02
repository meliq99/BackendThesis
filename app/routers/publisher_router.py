from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from typing import Annotated, Any, Dict
from utils.get_db_connection import get_session
from utils.publisher import publish_messages
import asyncio
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

@router.post("/start", status_code=status.HTTP_200_OK)
async def start_publisher(background_tasks: BackgroundTasks, session: SessionDependency) -> Dict[str, str]:
    """
    Start the background publishing task with a proper session.
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
    logger.info("Background publish task started")
    
    return {"status": "Publisher started"}

@router.post("/stop", status_code=status.HTTP_200_OK)
async def stop_publisher() -> Dict[str, str]:
    """
    Stop the background publishing task.
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
    
    return {"status": "Publisher stopped"} 
