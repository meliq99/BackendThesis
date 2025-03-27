import asyncio
import logging
from fastapi import FastAPI
from services.mqtt_service import MQTTService
from routers import data_router
from utils.publisher import publish_messages
from utils.get_db_connection import create_db_and_tables, check_initial_config
from routers import settings_router, simulation_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()
mqtt_service = MQTTService()
app.include_router(data_router.router)

# Assign the service to the router (or use dependency injection)
data_router.mqtt_service = mqtt_service

publish_task = None

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    check_initial_config()


    global publish_task
    # Start the background publish task
    # publish_task = asyncio.create_task(publish_messages(mqtt_service))
    # logger.info("Background publish task started.")

@app.on_event("shutdown")
async def shutdown_event():
    global publish_task
    if publish_task:
        publish_task.cancel()
        try:
            await publish_task
            logger.info("Background publish task cancelled successfully.")
        except asyncio.CancelledError:
            logger.info("Background publish task has been cancelled.")
    mqtt_service.disconnect()

app.include_router(settings_router.router)
app.include_router(simulation_router.router)