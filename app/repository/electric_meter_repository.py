from models.electric_meter_models import ElectricMeter
import uuid

def create_electric_meter(electric_meter: ElectricMeter, session):
    session.add(electric_meter)
    session.commit()
    session.refresh(electric_meter)
    return electric_meter