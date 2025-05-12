from models.current_status import CurrentStatus
import uuid
from sqlmodel import Session, select

def record_current_status(status: CurrentStatus, session) -> CurrentStatus:
    session.add(status)
    session.commit()
    session.refresh(status)
    return status


def change_current_status(simulation_id: uuid.UUID, status: str, session:Session) -> CurrentStatus:
    result = session.exec(select(CurrentStatus).where(CurrentStatus.id == simulation_id)).first()
    result.status = status
    session.add(result)
    session.commit()
    session.refresh(result)
    return result

def get_current_status(simulation_id: uuid.UUID,  session:Session) -> CurrentStatus:
    result = session.exec(select(CurrentStatus).where(CurrentStatus.id == simulation_id)).first()
    return result