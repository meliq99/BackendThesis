from models.settings_models import Device
from repository.settings_repository import create_device, get_devices, get_first_active_simulation



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
    # new_electric_meter = ElectricMeter(
    #     name = medidor.name,
    #     simulation_id = simulation.id,
    # )
    return {"devices": devices, "simulation": simulation}
    