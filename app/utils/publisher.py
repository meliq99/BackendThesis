import asyncio
import logging
import random
from models.data_model import DataModel

logger = logging.getLogger(__name__)

async def publish_messages(mqtt_service, interval: float = 5.0):
    """
    Background task to publish messages to the MQTT broker at regular intervals.
    """
    while True:
        try:
            data = DataModel(value=random.randint(0, 100))
            mqtt_service.publish(data.dict())
            logger.info(f"Published data: {data}")
        except Exception as e:
            logger.error(f"Error publishing data: {e}")
        await asyncio.sleep(interval)