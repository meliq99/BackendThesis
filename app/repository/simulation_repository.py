from models.simulation_models import Simulation
import uuid
from sqlmodel import Session, select
from models.simulation_models import ConsumptionAlgorithm

def create_simulation(simulation: Simulation, session):
    session.add(simulation)
    session.commit()
    session.refresh(simulation)
    return simulation

def desactive_simulation(simulation_id: uuid.UUID,session):
    simulation = session.get(Simulation, simulation_id)
    print(simulation)
    if simulation:
        simulation.is_active = False
        session.add(simulation)
        session.commit()
        session.refresh(simulation)
    return simulation

def get_consumtion_algorithms(session: Session):
    return session.exec(select(ConsumptionAlgorithm)).all()
    
def get_consumption_algorithm_by_id(algorithm_id: uuid.UUID, session: Session):
    statement = select(ConsumptionAlgorithm).where(ConsumptionAlgorithm.id == algorithm_id)
    return session.exec(statement).first()