from models.settings_models import Device
from repository.settings_repository import create_device, get_devices, get_first_active_simulation
from repository.electric_meter_repository import get_electric_meter
from repository.simulation_repository import get_consumtion_algorithms
from repository.settings_repository import delete_device
import uuid
async def create_device_service(device: Device, session):
    new_device = Device (name=device.name, 
                         description=device.description, 
                         consumption_value=device.consumption_value, 
                         icon=device.icon,
                         algorithm_id=device.algorithm_id, 
                         is_default=device.is_default,
                         peak_consumption=device.peak_consumption,
                         cycle_duration=device.cycle_duration,
                         on_duration=device.on_duration)
    
    return create_device(new_device, session)

async def delete_device_service(device_id: uuid.UUID, session):
    delete_device(device_id, session)
    return {"message": "Device deleted successfully"}

async def get_settings_service(session):
    devices = get_devices(session)
    simulation = get_first_active_simulation(session)
    electric_meter = get_electric_meter(simulation.id, session)
    consumption_algorithms = get_consumtion_algorithms(session)
    simulation_response = {
        "id": simulation.id,
        "name": simulation.name,
        "start_date": simulation.start_date,
        "update_date": simulation.update_date,
        "is_active": simulation.is_active,
        "electric_meter_id": electric_meter.id if electric_meter else None
    }
    return {"devices": devices, "simulation": simulation_response, "consumption_algorithms": consumption_algorithms}
    