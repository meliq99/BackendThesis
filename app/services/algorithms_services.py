from repository.algorithms_repository import (
    create_algorithm,
    get_algorithms,
    get_algorithm_by_id,
    update_algorithm,
    delete_algorithm
)
from schemes.algorithms_schemes import AlgorithmCreate, AlgorithmUpdate, AlgorithmResponse
import uuid
from sqlmodel import Session

async def create_algorithm_service(algorithm: AlgorithmCreate, session: Session) -> AlgorithmResponse:
    """Create a new consumption algorithm"""
    db_algorithm = create_algorithm(algorithm, session)
    return AlgorithmResponse(
        id=db_algorithm.id,
        name=db_algorithm.name,
        description=db_algorithm.description,
        algorithm_type=db_algorithm.algorithm_type,
        script=db_algorithm.script
    )

async def get_algorithms_service(session: Session) -> list[AlgorithmResponse]:
    """Get all consumption algorithms"""
    algorithms = get_algorithms(session)
    return [
        AlgorithmResponse(
            id=algorithm.id,
            name=algorithm.name,
            description=algorithm.description,
            algorithm_type=algorithm.algorithm_type,
            script=algorithm.script
        )
        for algorithm in algorithms
    ]

async def get_algorithm_service(algorithm_id: uuid.UUID, session: Session) -> AlgorithmResponse | None:
    """Get a consumption algorithm by ID"""
    algorithm = get_algorithm_by_id(algorithm_id, session)
    if not algorithm:
        return None
    
    return AlgorithmResponse(
        id=algorithm.id,
        name=algorithm.name,
        description=algorithm.description,
        algorithm_type=algorithm.algorithm_type,
        script=algorithm.script
    )

async def update_algorithm_service(algorithm_id: uuid.UUID, algorithm: AlgorithmUpdate, session: Session) -> AlgorithmResponse | None:
    """Update a consumption algorithm"""
    db_algorithm = update_algorithm(algorithm_id, algorithm, session)
    if not db_algorithm:
        return None
    
    return AlgorithmResponse(
        id=db_algorithm.id,
        name=db_algorithm.name,
        description=db_algorithm.description,
        algorithm_type=db_algorithm.algorithm_type,
        script=db_algorithm.script
    )

async def delete_algorithm_service(algorithm_id: uuid.UUID, session: Session) -> bool:
    """Delete a consumption algorithm"""
    return delete_algorithm(algorithm_id, session)
