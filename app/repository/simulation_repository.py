from models.simulation_models import Simulation
import uuid
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
    