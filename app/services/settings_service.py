from models.settings_models import Device
from repository.settings_repository import create_device, get_devices, get_first_active_simulation, get_electric_meter



async def create_device_service(device: Device, session):
    new_device = Device(name=device.name, 
                         description=device.description, 
                         consumption_value=device.consumption_value, 
                         consumption_algorithm=device.consumption_algorithm, 
                         is_default=device.is_default)
    return create_device(new_device, session)


async def get_settings_service(session):
    devices = get_devices(session)
    simulation = get_first_active_simulation(session)
    electric_meter = get_electric_meter(session, simulation.id)
    simulation_response = {
        "id": simulation.id,
        "name": simulation.name,
        "start_date": simulation.start_date,
        "update_date": simulation.update_date,
        "is_active": simulation.is_active,
        "electric_meter_id": electric_meter.id if electric_meter else None
    }
    return {"devices": devices, "simulation": simulation_response}
    