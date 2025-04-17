import json
import time
import paho.mqtt.client as mqtt
import logging

# Configure logging for detailed output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self, host='localhost', port=15675, topic='test/mqtt'):
        self.host = host
        self.port = port
        self.topic = topic
        # Use WebSockets transport and set the WebSocket path to /ws
        self.client = mqtt.Client(transport="websockets")
        self.client.ws_set_options(path="/ws")
        # Use guest credentials
        self.client.username_pw_set("guest", "guest")
        
        # Enable logging for Paho MQTT
        self.client.enable_logger(logger)
        
        # Assign callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
        # Initialize connection
        self.connect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker via WebSockets")
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning(f"Unexpected disconnection. Return code: {rc}")
            self.reconnect()

    def connect(self):
        max_retries = 5
        delay = 5
        retries = 0
        while retries < max_retries:
            try:
                self.client.connect(self.host, self.port, keepalive=60)
                self.client.loop_start()
                logger.info("MQTT loop started")
                return
            except Exception as e:
                logger.error(f"Connection attempt {retries + 1} failed: {e}")
                retries += 1
                if retries < max_retries:
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
        raise ConnectionError("Failed to connect to MQTT Broker after multiple attempts.")

    def reconnect(self):
        logger.info("Attempting to reconnect...")
        try:
            self.client.reconnect()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")

    def publish(self, message):
        if not self.client.is_connected():
            logger.warning("MQTT client is not connected. Attempting to reconnect...")
            self.reconnect()
            if not self.client.is_connected():
                raise ConnectionError("Cannot publish because MQTT client is not connected.")
        
        payload = json.dumps(message)
        result = self.client.publish(self.topic, payload)
        status = result[0]
        if status == 0:
            logger.info(f"Sent `{payload}` to topic `{self.topic}`")
        else:
            logger.error(f"Failed to send message to topic `{self.topic}`")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT Broker")
