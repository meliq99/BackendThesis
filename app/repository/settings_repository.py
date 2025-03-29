from models.settings_models import Device
from sqlmodel import select
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

def get_electric_meter(session, simulation_id: uuid.UUID) -> ElectricMeter:
   
    electric_meter_statement = select(ElectricMeter).where(ElectricMeter.simulation_id == simulation_id)
    return session.exec(electric_meter_statement).first() 


