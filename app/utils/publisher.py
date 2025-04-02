import asyncio
import logging
from models.data_model import DataModel
from services import simulation_service
from repository import electric_meter_repository, device_simulation_repository, simulation_repository
from schemes import device_simulation_schemes, electric_meter_schemes
from uuid import UUID
from sqlmodel import Session

logger = logging.getLogger(__name__)

async def get_current_electric_meter(session: Session):
    current_active_simulation = simulation_service.get_first_active_simulation(session)
    current_electric_meter = electric_meter_repository.get_electric_meter(current_active_simulation.id, session)
    return current_electric_meter

async def get_current_device_simulations(session: Session):
    current_electric_meter = await get_current_electric_meter(session)
    current_device_simulations = device_simulation_repository.get_device_simulations(current_electric_meter.id, session)
    return current_device_simulations

async def get_consumption_algorithms(algorithm_id: UUID, session: Session):
    result = simulation_repository.get_consumption_algorithm_by_id(algorithm_id, session)
    return result.script

async def calculate_consumption(devices_simulation: list[device_simulation_schemes.DeviceSimulation], current_electric_meter: electric_meter_schemes.ElectricMeter, session):
    devices_consumption = 0
    for device_simulation in devices_simulation:
        consumption_algorithm = await get_consumption_algorithms(device_simulation.algorithm_id, session)
        print("consumption_algorithm", consumption_algorithm)
        devices_consumption += device_simulation.consumption_value

    return devices_consumption + current_electric_meter.base_comsumption


async def publish_messages(mqtt_service, session, interval: float = 2.0):
    """
    Background task to publish messages to the MQTT broker at regular intervals.
    """
    while True:
        try:
            current_device_simulations = await get_current_device_simulations(session)
            current_electric_meter = await get_current_electric_meter(session)
            consumption = await calculate_consumption(current_device_simulations, current_electric_meter, session)
            data = DataModel(value=consumption)
            mqtt_service.publish(data.dict())
            logger.info(f"Published data: {data}")
        except Exception as e:
            logger.error(f"Error publishing data: {e}")
        await asyncio.sleep(interval)