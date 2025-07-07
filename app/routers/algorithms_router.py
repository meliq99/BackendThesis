from fastapi import APIRouter, status, Depends, HTTPException
from schemes.algorithms_schemes import AlgorithmCreate, AlgorithmUpdate, AlgorithmResponse
from typing import Any, Annotated
from utils.get_db_connection import get_session
from services import algorithms_services
import uuid

router = APIRouter(
    prefix="/algorithms",
    tags=["algorithms"],
)

SessionDependency = Annotated[Any, Depends(get_session)]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AlgorithmResponse)
async def create_algorithm(algorithm: AlgorithmCreate, session: SessionDependency) -> Any:
    """Create a new consumption algorithm"""
    try:
        new_algorithm = await algorithms_services.create_algorithm_service(algorithm, session)
        return new_algorithm
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create algorithm: {str(e)}"
        )

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AlgorithmResponse])
async def get_algorithms(session: SessionDependency) -> Any:
    """Get all consumption algorithms"""
    return await algorithms_services.get_algorithms_service(session)

@router.get("/{algorithm_id}", status_code=status.HTTP_200_OK, response_model=AlgorithmResponse)
async def get_algorithm(algorithm_id: uuid.UUID, session: SessionDependency) -> Any:
    """Get a consumption algorithm by ID"""
    algorithm = await algorithms_services.get_algorithm_service(algorithm_id, session)
    if not algorithm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algorithm not found"
        )
    return algorithm

@router.put("/{algorithm_id}", status_code=status.HTTP_200_OK, response_model=AlgorithmResponse)
async def update_algorithm(algorithm_id: uuid.UUID, algorithm: AlgorithmUpdate, session: SessionDependency) -> Any:
    """Update a consumption algorithm"""
    try:
        updated_algorithm = await algorithms_services.update_algorithm_service(algorithm_id, algorithm, session)
        if not updated_algorithm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Algorithm not found"
            )
        return updated_algorithm
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update algorithm: {str(e)}"
        )

@router.delete("/{algorithm_id}", status_code=status.HTTP_200_OK)
async def delete_algorithm(algorithm_id: uuid.UUID, session: SessionDependency) -> Any:
    """Delete a consumption algorithm"""
    success = await algorithms_services.delete_algorithm_service(algorithm_id, session)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algorithm not found"
        )
    return {"message": "Algorithm deleted successfully"} 