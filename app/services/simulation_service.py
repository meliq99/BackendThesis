from models.simulation_models import Simulation
from models.electric_meter_models import ElectricMeter
from repository.simulation_repository import create_simulation, desactive_simulation
from repository.settings_repository import get_first_active_simulation
from repository.electric_meter_repository import create_electric_meter


async def create_simulation_service(simulation: Simulation, session):
    new_simulation = Simulation(name=simulation.name, 
                                start_date=simulation.start_date, 
                                update_date=simulation.update_date, 
                                is_active=simulation.is_active)
    current_simulation = get_first_active_simulation(session)

    new_simulation_created = create_simulation(new_simulation, session)

    if new_simulation_created:
        new_default_electric_meter = create_electric_meter(ElectricMeter(base_comsumption=0, 
                                            simulation_id=new_simulation_created.id), 
                                            session)
        new_simulation_created = {
        "id": new_simulation_created.id,
        "name": new_simulation_created.name,
        "start_date": new_simulation_created.start_date,
        "update_date": new_simulation_created.update_date,
        "is_active": new_simulation_created.is_active,
        "electric_meter_id": new_default_electric_meter.id if new_default_electric_meter else None
    }

    if (current_simulation.is_active and new_simulation_created):
        desactive_simulation(current_simulation.id, session)
        return new_simulation_created
    elif not new_simulation_created:
        return current_simulation
    return new_simulation_created

