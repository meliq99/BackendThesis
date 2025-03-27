from models.simulation_models import Simulation
from repository.simulation_repository import create_simulation

async def create_simulation_service(simulation: Simulation, session):
    new_simulation = Simulation(name=simulation.name, 
                                start_date=simulation.start_date, 
                                update_date=simulation.update_date, 
                                is_active=simulation.is_active)
    return create_simulation(new_simulation, session)