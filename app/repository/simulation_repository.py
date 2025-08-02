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

def get_simulation_by_id(simulation_id: uuid.UUID, session: Session):
    """Get simulation by ID."""
    return session.get(Simulation, simulation_id)

def get_active_simulation(session: Session):
    """Get the currently active simulation."""
    statement = select(Simulation).where(Simulation.is_active == True)
    return session.exec(statement).first()

def update_simulation(simulation_id: uuid.UUID, update_data: dict, session: Session):
    """Update simulation with new data."""
    simulation = session.get(Simulation, simulation_id)
    if not simulation:
        return None
    
    # Update only provided fields
    for field, value in update_data.items():
        if value is not None:
            setattr(simulation, field, value)
    
    session.add(simulation)
    session.commit()
    session.refresh(simulation)
    return simulation