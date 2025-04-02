from models.settings_models import Device
from repository.settings_repository import create_device, get_devices, get_first_active_simulation
from repository.electric_meter_repository import get_electric_meter
from repository.simulation_repository import get_consumtion_algorithms

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
    