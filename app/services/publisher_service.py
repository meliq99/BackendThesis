import uuid
from repository.publisher_repository import record_current_status, change_current_status, get_current_status
from models.current_status import CurrentStatus

async def get_status_service(simulation_id: uuid.UUID, session):
    return get_current_status(simulation_id, session)


async def save_status_service(simulation_id: uuid.UUID, status: str, session):
    current_simulation_status = get_current_status(simulation_id, session)
    print("jsgdcy", current_simulation_status)
    if not current_simulation_status:
        new_record = CurrentStatus(
            id = simulation_id,
            status= status
        )
        return record_current_status(new_record, session)
    
    return change_current_status(simulation_id, status, session)