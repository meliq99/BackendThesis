import asyncio
import logging
from fastapi import FastAPI
from services.mqtt_service import MQTTService
from routers import data_router
from utils.get_db_connection import create_db_and_tables, check_initial_config
from routers import settings_router, simulation_router, device_simulation_router, publisher_router
from utils.get_db_connection import get_session
from typing import Annotated, Any
from fastapi import Depends
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mqtt_service = MQTTService()
app.include_router(data_router.router)

# Assign the service to the router (or use dependency injection)
data_router.mqtt_service = mqtt_service
publisher_router.mqtt_service = mqtt_service


@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    check_initial_config()
    logger.info("Application startup complete.")


@app.on_event("shutdown")
async def shutdown_event():
    mqtt_service.disconnect()
    logger.info("Application shutdown complete.")


app.include_router(settings_router.router)
app.include_router(simulation_router.router)
app.include_router(device_simulation_router.router)
app.include_router(publisher_router.router)
