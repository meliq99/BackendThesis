from models.settings_models import Device
from repository.settings_repository import create_device
import uuid


async def create_device_service(device: Device, session):
    new_device = Device(name=device.name, 
                         description=device.description, 
                         consumption_value=device.consumption_value, 
                         consumption_algorithm=device.consumption_algorithm, 
                         is_default=device.is_default)
    return create_device(new_device, session)



    