from models.algorithms_models import ConsumptionAlgorithm
from schemes.algorithms_schemes import AlgorithmCreate, AlgorithmUpdate
import uuid
from sqlmodel import Session, select

def create_algorithm(algorithm: AlgorithmCreate, session: Session) -> ConsumptionAlgorithm:
    """Create a new consumption algorithm"""
    db_algorithm = ConsumptionAlgorithm(
        name=algorithm.name,
        description=algorithm.description,
        algorithm_type=algorithm.algorithm_type,
        script=algorithm.script
    )
    session.add(db_algorithm)
    session.commit()
    session.refresh(db_algorithm)
    return db_algorithm

def get_algorithms(session: Session) -> list[ConsumptionAlgorithm]:
    """Get all consumption algorithms"""
    return session.exec(select(ConsumptionAlgorithm)).all()

def get_algorithm_by_id(algorithm_id: uuid.UUID, session: Session) -> ConsumptionAlgorithm | None:
    """Get a consumption algorithm by ID"""
    statement = select(ConsumptionAlgorithm).where(ConsumptionAlgorithm.id == algorithm_id)
    return session.exec(statement).first()

def update_algorithm(algorithm_id: uuid.UUID, algorithm: AlgorithmUpdate, session: Session) -> ConsumptionAlgorithm | None:
    """Update a consumption algorithm"""
    db_algorithm = session.exec(select(ConsumptionAlgorithm).where(ConsumptionAlgorithm.id == algorithm_id)).first()
    if not db_algorithm:
        return None
    
    algorithm_data = algorithm.dict(exclude_unset=True)
    for key, value in algorithm_data.items():
        setattr(db_algorithm, key, value)
    
    session.add(db_algorithm)
    session.commit()
    session.refresh(db_algorithm)
    return db_algorithm

def delete_algorithm(algorithm_id: uuid.UUID, session: Session) -> bool:
    """Delete a consumption algorithm"""
    db_algorithm = session.exec(select(ConsumptionAlgorithm).where(ConsumptionAlgorithm.id == algorithm_id)).first()
    if not db_algorithm:
        return False
    
    session.delete(db_algorithm)
    session.commit()
    return True
