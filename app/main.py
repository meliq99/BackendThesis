from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mqtt_client import MQTTClient
import logging
import asyncio
import random  # Optional: for generating random data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
mqtt_client = None
publish_task = None  # To hold the background task

# Define a data model using Pydantic
class DataModel(BaseModel):
    value: int

async def publish_messages(interval: float = 5.0):
    """
    Background task to publish messages to the MQTT broker at regular intervals.
    
    :param interval: Time in seconds between each publish.
    """
    while True:
        if mqtt_client and mqtt_client.client.is_connected():
            try:
                # Generate or retrieve the data to send
                data = DataModel(value=random.randint(0, 100))  # Example with random data
                mqtt_client.publish(data.dict())
                logger.info(f"Published data: {data}")
            except Exception as e:
                logger.error(f"Error publishing data: {e}")
        else:
            logger.warning("MQTT client is not connected. Skipping publish.")
        await asyncio.sleep(interval)

@app.on_event("startup")
async def startup_event():
    global mqtt_client, publish_task
    try:
        mqtt_client = MQTTClient()
        logger.info("MQTT Client initialized successfully.")
        
        # Start the background publish task
        publish_task = asyncio.create_task(publish_messages())
        logger.info("Background publish task started.")
    except Exception as e:
        logger.error(f"Error initializing MQTT Client: {e}")
        mqtt_client = None

@app.post("/send-data/")
async def send_data(data: DataModel):
    if not mqtt_client:
        logger.error("MQTT client is not initialized.")
        raise HTTPException(status_code=500, detail="MQTT client not initialized.")
    try:
        message = data.dict()
        mqtt_client.publish(message)
        return {"status": "Message sent to MQTT Broker", "data": message}
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    global mqtt_client, publish_task
    if publish_task:
        publish_task.cancel()
        try:
            await publish_task
            logger.info("Background publish task cancelled successfully.")
        except asyncio.CancelledError:
            logger.info("Background publish task has been cancelled.")
    if mqtt_client:
        mqtt_client.disconnect()
        logger.info("MQTT Client disconnected successfully.")
