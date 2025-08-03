import asyncio
import logging
import time
from models.data_model import DataModel
from services import simulation_service
from repository import electric_meter_repository, device_simulation_repository, simulation_repository
from schemes import device_simulation_schemes, electric_meter_schemes
from utils.unit_converter import watts_to_unit, PowerUnit, get_time_multiplier, TimeUnit
from uuid import UUID
from sqlmodel import Session

logger = logging.getLogger(__name__)

async def get_simulation_unit(session: Session) -> str:
    """
    Helper function to get the current simulation's output unit.
    This function ensures fresh data by expiring the session cache.
    """
    simulation = await get_current_simulation(session)
    return simulation.output_unit if simulation else "W"


def calculate_simulation_time(simulation) -> int:
    """
    Calculate current simulation time based on speed and start time configuration.
    
    Args:
        simulation: Current simulation object with time configuration
        
    Returns:
        Current simulation time as Unix timestamp (seconds)
    """
    real_time = time.time()
    
    if simulation.simulation_start_time:
        # Use custom start time with speed multiplier
        start_timestamp = simulation.simulation_start_time.timestamp()
        elapsed_real = real_time - start_timestamp
        elapsed_simulation = elapsed_real * simulation.time_speed
        return int(start_timestamp + elapsed_simulation)
    else:
        # Use current real time with speed multiplier
        # Note: For speed > 1.0, this accelerates time
        # For speed < 1.0, this slows down time
        return int(real_time * simulation.time_speed)

def execute_custom_simulation(custom_script: str, current_time: int, base_consumption: float, peak_consumption: float, cycle_duration:int, on_duration: int, extra_params:dict={}) -> float:
    """
        Ejecuta un script custom que define una función `simulate` para calcular el consumo.
        La función `simulate` debe tener la siguiente firma:
        
            simulate(current_time: int, base_consumption: float, peak_consumption: float,
                    cycle_duration: int, on_duration: int, extra_params: dict) -> float
        """
    exec_env ={}
    exec(custom_script,{}, exec_env)

    if "simulate" not in exec_env:
        raise ValueError("El script debe definir una función 'simulate'.")
    
    simulate_func = exec_env["simulate"]
    return simulate_func(current_time, base_consumption, peak_consumption, cycle_duration, on_duration, extra_params)


async def get_current_simulation(session: Session):
    # Expire all cached objects to ensure fresh data from database
    session.expire_all()
    current_active_simulation = simulation_service.get_first_active_simulation(session)
    return current_active_simulation

async def get_current_electric_meter(session: Session):
    current_active_simulation = await get_current_simulation(session)
    current_electric_meter = electric_meter_repository.get_electric_meter(current_active_simulation.id, session)
    return current_electric_meter

async def get_current_device_simulations(session: Session):
    current_electric_meter = await get_current_electric_meter(session)
    current_device_simulations = device_simulation_repository.get_device_simulations(current_electric_meter.id, session)
    return current_device_simulations

async def get_consumption_algorithms(algorithm_id: UUID, session: Session):
    result = simulation_repository.get_consumption_algorithm_by_id(algorithm_id, session)
    return result.script

# async def calculate_consumption(devices_simulation: list[device_simulation_schemes.DeviceSimulation], current_electric_meter: electric_meter_schemes.ElectricMeter, session):
#     devices_consumption = 0
#     for device_simulation in devices_simulation:
#         consumption_algorithm = await get_consumption_algorithms(device_simulation.algorithm_id, session)
#         print("consumption_algorithm", consumption_algorithm)
#         devices_consumption += device_simulation.consumption_value

#     return devices_consumption + current_electric_meter.base_consumption

async def calculate_consumption(devices_simulation: list[device_simulation_schemes.DeviceSimulation], current_electric_meter: electric_meter_schemes.ElectricMeter, session: Session) -> float:
    devices_consumption = 0
    
    # Get current simulation for time configuration
    simulation = await get_current_simulation(session)
    
    # Calculate simulation time based on configuration
    simulation_time = calculate_simulation_time(simulation)
    
    # Get time unit multiplier for algorithms
    time_multiplier = get_time_multiplier(simulation.time_unit)

    for device_simulation in devices_simulation:
        custom_script = await get_consumption_algorithms(device_simulation.algorithm_id, session)
        try:
            # Prepare extra_params with time configuration
            extra_params = {
                "base_interval": time_multiplier,
                "time_unit": simulation.time_unit,
                "time_speed": simulation.time_speed,
                "factor": 1.0  # Default factor, can be customized per device later
            }
            
            device_consumption = execute_custom_simulation(
                custom_script=custom_script,
                current_time=simulation_time,
                base_consumption=device_simulation.consumption_value,
                peak_consumption=device_simulation.peak_consumption,
                cycle_duration=device_simulation.cycle_duration,
                on_duration=device_simulation.on_duration,
                extra_params=extra_params
            )
            logger.debug(f"Device {device_simulation.id} consumption: {device_consumption}W (sim_time: {simulation_time})")
        except Exception as e:
            logger.error(f"Error executing custom simulation for device {device_simulation.id}: {e}")
            device_consumption = 0

        devices_consumption += device_consumption

    return devices_consumption + current_electric_meter.base_consumption

async def publish_messages(mqtt_service, session, interval: float = 2.0):
    """
    Background task to publish messages to the MQTT broker at regular intervals.
    Converts consumption from watts to the configured output unit before publishing.
    """
    while True:
        try:
            current_simulation = await get_current_simulation(session)
            current_device_simulations = await get_current_device_simulations(session)
            current_electric_meter = await get_current_electric_meter(session)
            
            # Calculate consumption in watts (internal unit)
            consumption_watts = await calculate_consumption(current_device_simulations, current_electric_meter, session)
            
            # Convert to the configured output unit for frontend
            output_unit = current_simulation.output_unit
            consumption_in_output_unit = watts_to_unit(consumption_watts, output_unit)
            
            # Calculate simulation time for timestamp
            simulation_time = calculate_simulation_time(current_simulation)
            
            # Create comprehensive data model with simulation parameters
            data = DataModel(
                value=consumption_in_output_unit,
                unit=output_unit,
                time_unit=current_simulation.time_unit,
                time_speed=current_simulation.time_speed,
                simulation_id=str(current_simulation.id),
                timestamp=simulation_time
            )
            mqtt_service.publish(data.dict())
            
            # Enhanced logging with time information
            logger.info(f"Published data: {consumption_in_output_unit} {output_unit} "
                       f"(time_unit: {current_simulation.time_unit}, time_speed: {current_simulation.time_speed}x, "
                       f"sim_time: {simulation_time}, simulation_id: {current_simulation.id})")
        except Exception as e:
            logger.error(f"Error publishing data: {e}")
        await asyncio.sleep(interval)

async def publish_message(mqtt_service, data):
    """
    Single message publish function. 
    Note: This function assumes data is already in the correct unit.
    """
    mqtt_service.publish(data)
    logger.info(f"Published data to {data['subject']}: {data['value']}")
    return data