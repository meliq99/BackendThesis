from models.electric_meter_models import ElectricMeter
from sqlmodel import select
import uuid

def create_electric_meter(electric_meter: ElectricMeter, session):
    session.add(electric_meter)
    session.commit()
    session.refresh(electric_meter)
    return electric_meter


def get_electric_meter(simulation_id: uuid.UUID, session) -> ElectricMeter:
    electric_meter_statement = select(ElectricMeter).where(ElectricMeter.simulation_id == simulation_id)
    return session.exec(electric_meter_statement).first() 