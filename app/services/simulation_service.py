from models.simulation_models import Simulation
from models.electric_meter_models import ElectricMeter
from repository.simulation_repository import create_simulation, desactive_simulation, update_simulation, get_simulation_by_id, get_active_simulation
from repository.settings_repository import get_first_active_simulation
from repository.electric_meter_repository import create_electric_meter
from schemes.simulation_schemes import SimulationUpdate


async def create_simulation_service(simulation: Simulation, session):
    new_simulation = Simulation(name=simulation.name, 
                                start_date=simulation.start_date, 
                                update_date=simulation.update_date, 
                                is_active=simulation.is_active,
                                output_unit=simulation.output_unit,
                                time_unit=simulation.time_unit,
                                time_speed=simulation.time_speed,
                                simulation_start_time=simulation.simulation_start_time)
    current_simulation = get_first_active_simulation(session)

    new_simulation_created = create_simulation(new_simulation, session)

    if new_simulation_created:
        new_default_electric_meter = create_electric_meter(ElectricMeter(base_consumption=0, 
                                            simulation_id=new_simulation_created.id), 
                                            session)
        new_simulation_created = {
        "id": new_simulation_created.id,
        "name": new_simulation_created.name,
        "start_date": new_simulation_created.start_date,
        "update_date": new_simulation_created.update_date,
        "is_active": new_simulation_created.is_active,
        "output_unit": new_simulation_created.output_unit,
        "time_unit": new_simulation_created.time_unit,
        "time_speed": new_simulation_created.time_speed,
        "simulation_start_time": new_simulation_created.simulation_start_time,
        "electric_meter_id": new_default_electric_meter.id if new_default_electric_meter else None
    }

    if (current_simulation.is_active and new_simulation_created):
        desactive_simulation(current_simulation.id, session)
        return new_simulation_created
    elif not new_simulation_created:
        return current_simulation
    return new_simulation_created

async def update_simulation_service(simulation_id, simulation_update: SimulationUpdate, session):
    """Update simulation parameters service."""
    
    # Convert SimulationUpdate to dict, excluding None values
    update_data = simulation_update.dict(exclude_none=True)
    
    if not update_data:
        # No updates provided, return current simulation
        simulation = get_simulation_by_id(simulation_id, session)
        if not simulation:
            return None
        return {
            "id": simulation.id,
            "name": simulation.name,
            "start_date": simulation.start_date,
            "update_date": simulation.update_date,
            "is_active": simulation.is_active,
            "output_unit": simulation.output_unit,
            "time_unit": simulation.time_unit,
            "time_speed": simulation.time_speed,
            "simulation_start_time": simulation.simulation_start_time
        }
    
    # Update the simulation
    updated_simulation = update_simulation(simulation_id, update_data, session)
    
    if not updated_simulation:
        return None
    
    return {
        "id": updated_simulation.id,
        "name": updated_simulation.name,
        "start_date": updated_simulation.start_date,
        "update_date": updated_simulation.update_date,
        "is_active": updated_simulation.is_active,
        "output_unit": updated_simulation.output_unit,
        "time_unit": updated_simulation.time_unit,
        "time_speed": updated_simulation.time_speed,
        "simulation_start_time": updated_simulation.simulation_start_time
    }

async def get_active_simulation_service(session):
    """Get the currently active simulation."""
    simulation = get_active_simulation(session)
    
    if not simulation:
        return None
    
    return {
        "id": simulation.id,
        "name": simulation.name,
        "start_date": simulation.start_date,
        "update_date": simulation.update_date,
        "is_active": simulation.is_active,
        "output_unit": simulation.output_unit,
        "time_unit": simulation.time_unit,
        "time_speed": simulation.time_speed,
        "simulation_start_time": simulation.simulation_start_time
    }

