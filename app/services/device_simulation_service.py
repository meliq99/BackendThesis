from repository.device_simulation_repository import create_device_simulation, get_device_simulations
from models.device_simulation_models import DeviceSimulation
from schemes.device_simulation_schemes import DeviceSimulation as DeviceSimulationSchema
import uuid

async def create_device_simulation_service(device_simulation: DeviceSimulationSchema, session):
    db_device_simulation = DeviceSimulation(
        name= device_simulation.name,
        description= device_simulation.description,
        consumption_value= device_simulation.consumption_value,
        consumption_algorithm= device_simulation.consumption_algorithm,
        is_default= device_simulation.is_default,
        electric_meter_id= device_simulation.electric_meter_id
    )
    return create_device_simulation(db_device_simulation, session)

async def get_device_simulations_service(electric_meter_id: uuid.UUID, session) -> list[DeviceSimulation]:
    return get_device_simulations(electric_meter_id, session)

