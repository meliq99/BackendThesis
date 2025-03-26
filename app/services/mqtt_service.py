import logging
from mqtt_client import MQTTClient

logger = logging.getLogger(__name__)

class MQTTService:
    def __init__(self):
        try:
            self.client = MQTTClient()
            logger.info("MQTT Client initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing MQTT Client: {e}")
            self.client = None

    def publish(self, message: dict):
        if self.client and self.client.client.is_connected():
            self.client.publish(message)
        else:
            raise ConnectionError("MQTT client is not connected.")

    def disconnect(self):
        if self.client:
            self.client.disconnect()
            logger.info("MQTT Client disconnected successfully.")