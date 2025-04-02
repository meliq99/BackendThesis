from models.device_simulation_models import DeviceSimulation
import uuid
from sqlmodel import select, Session

def create_device_simulation(device_simulation: DeviceSimulation, session) -> DeviceSimulation:
    session.add(device_simulation)
    session.commit()
    session.refresh(device_simulation)
    return device_simulation

def get_device_simulations(electric_meter_id: uuid.UUID, session: Session) -> list[DeviceSimulation]:
    result = select(DeviceSimulation).where(DeviceSimulation.electric_meter_id == electric_meter_id)
    return session.exec(result).all()

def delete_device_simulation(device_simulation_id: uuid.UUID, session: Session) -> None:
    result = session.exec(select(DeviceSimulation).where(DeviceSimulation.id == device_simulation_id)).one()
    session.delete(result)
    session.commit()

def update_device_simulation(device_simulation_id: uuid.UUID, device_simulation: DeviceSimulation, session: Session) -> None:
    result = session.exec(select(DeviceSimulation).where(DeviceSimulation.id == device_simulation_id)).one()
    result.name = device_simulation.name
    result.description = device_simulation.description
    result.consumption_value = device_simulation.consumption_value
    result.peak_consumption = device_simulation.peak_consumption
    result.cycle_duration = device_simulation.cycle_duration
    result.on_duration = device_simulation.on_duration
    result.algorithm_id = device_simulation.algorithm_id
    session.add(result)
    session.commit()
    session.refresh(result)
    return result

