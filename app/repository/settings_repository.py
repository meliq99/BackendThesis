from models.settings_models import Device
from sqlmodel import select, Session
from models.simulation_models import Simulation
from models.electric_meter_models import ElectricMeter
import uuid

def create_device(device: Device, session) -> Device:
    session.add(device)
    session.commit()
    session.refresh(device)
    return device

def get_devices(session) -> list[Device]:
    return session.query(Device).all()

def get_first_active_simulation(session) -> Simulation:
    simulation_statement = select(Simulation).where(Simulation.is_active == True)
    return session.exec(simulation_statement).first()

def delete_device(device_id: uuid.UUID, session) -> None:
    result = session.exec(select(Device).where(Device.id == device_id)).one()
    session.delete(result)
    session.commit()

def update_device(device_id: uuid.UUID, device: Device, session: Session) -> None:
    result = session.exec(select(Device).where(Device.id == device_id)).one()
    result.name = device.name
    result.description = device.description
    result.consumption_value = device.consumption_value
    result.icon = device.icon
    result.is_default = device.is_default
    result.peak_consumption = device.peak_consumption
    result.cycle_duration = device.cycle_duration
    result.on_duration = device.on_duration
    result.algorithm_id = device.algorithm_id
    session.add(result)
    session.commit()
    session.refresh(result)
    return result