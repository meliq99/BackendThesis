from models.simulation_models import Simulation

def create_simulation(simulation: Simulation, session):
    session.add(simulation)
    session.commit()
    session.refresh(simulation)
    return simulation