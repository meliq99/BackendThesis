from models.simulation_models import Simulation
from repository.simulation_repository import create_simulation, desactive_simulation
from repository.settings_repository import get_first_active_simulation


async def create_simulation_service(simulation: Simulation, session):
    new_simulation = Simulation(name=simulation.name, 
                                start_date=simulation.start_date, 
                                update_date=simulation.update_date, 
                                is_active=simulation.is_active)
    current_simulation = get_first_active_simulation(session)

    new_simulation_created = create_simulation(new_simulation, session)

    if (current_simulation.is_active and new_simulation_created):
        desactive_simulation(current_simulation.id, session)
        return new_simulation_created
    elif not new_simulation_created:
        return current_simulation
    return new_simulation_created


