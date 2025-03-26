from fastapi import APIRouter, HTTPException
from models.data_model import DataModel

router = APIRouter()

# Assume that mqtt_service is set up and passed to the router via dependency injection or global state.
mqtt_service = None  # You can set this in your main startup event

# @router.post("/send-data/")
# async def send_data(data: DataModel):
#     if not mqtt_service:
#         raise HTTPException(status_code=500, detail="MQTT client not initialized.")
#     try:
#         message = data.dict()
#         mqtt_service.publish(message)
#         return {"status": "Message sent to MQTT Broker", "data": message}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")