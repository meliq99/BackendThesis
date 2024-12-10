from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mqtt_client import MQTTClient
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
mqtt_client = None

# Define a data model using Pydantic
class DataModel(BaseModel):
    value: int

@app.on_event("startup")
def startup_event():
    global mqtt_client
    try:
        mqtt_client = MQTTClient()
        logger.info("MQTT Client initialized successfully.")
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
def shutdown_event():
    if mqtt_client:
        mqtt_client.disconnect()
        logger.info("MQTT Client disconnected successfully.")
