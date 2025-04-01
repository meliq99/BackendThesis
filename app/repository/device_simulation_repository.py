from models.device_simulation_models import DeviceSimulation
import uuid
from sqlmodel import select
def create_device_simulation(device_simulation: DeviceSimulation, session) -> DeviceSimulation:
    session.add(device_simulation)
    session.commit()
    session.refresh(device_simulation)
    return device_simulation

def get_device_simulations(electric_meter_id: uuid.UUID, session) -> list[DeviceSimulation]:
    result = select(DeviceSimulation).where(DeviceSimulation.electric_meter_id == electric_meter_id)
    return session.exec(result).all()


