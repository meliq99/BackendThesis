from repository.device_simulation_repository import create_device_simulation, get_device_simulations, delete_device_simulation, update_device_simulation
from models.device_simulation_models import DeviceSimulation
from schemes.device_simulation_schemes import DeviceSimulation as DeviceSimulationSchema
import uuid

async def create_device_simulation_service(device_simulation: DeviceSimulationSchema, session):
    db_device_simulation = DeviceSimulation(
        name= device_simulation.name,
        description= device_simulation.description,
        consumption_value= device_simulation.consumption_value,
        icon=device_simulation.icon,
        is_default= device_simulation.is_default,
        peak_consumption=device_simulation.peak_consumption,
        cycle_duration=device_simulation.cycle_duration,
        on_duration=device_simulation.on_duration,
        algorithm_id=device_simulation.algorithm_id,
        electric_meter_id= device_simulation.electric_meter_id
    )
    return create_device_simulation(db_device_simulation, session)

async def get_device_simulations_service(electric_meter_id: uuid.UUID, session) -> list[DeviceSimulation]:
    return get_device_simulations(electric_meter_id, session)


async def delete_device_simulation_service(device_simulation_id: uuid.UUID, session) -> None:
    delete_device_simulation(device_simulation_id, session)
    return {"message": "Device simulation deleted successfully"}

async def update_device_simulation_service(device_simulation_id: uuid.UUID, device_simulation: DeviceSimulationSchema, session) -> None:
    db_device_simulation = DeviceSimulation(
        name= device_simulation.name,
        description= device_simulation.description,
        consumption_value= device_simulation.consumption_value,
        icon= device_simulation.icon,
        peak_consumption=device_simulation.peak_consumption,
        cycle_duration=device_simulation.cycle_duration,
        on_duration=device_simulation.on_duration,
        algorithm_id=device_simulation.algorithm_id,
    )
    return update_device_simulation(device_simulation_id, db_device_simulation, session)    
