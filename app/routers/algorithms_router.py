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
    """
    Create a new consumption algorithm for device energy simulation.
    
    Algorithms define how devices consume energy over time, including patterns
    like constant consumption, cyclical behavior, or variable usage.
    
    Example request:
    ```json
    {
        "name": "Washing Machine Cycle",
        "description": "Energy pattern for washing machine cycles",
        "algorithm_type": "cyclical",
        "parameters": {
            "base_consumption": 500,
            "peak_consumption": 2000,
            "cycle_duration": 90,
            "on_duration": 60
        }
    }
    ```
    
    Returns:
    - Created algorithm with generated ID
    - All algorithm parameters and metadata
    - Timestamps for creation tracking
    """
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
    """
    Retrieve all available consumption algorithms.
    
    Returns a comprehensive list of all algorithms in the system,
    including their configurations and usage parameters.
    
    Returns:
    - List of all algorithms with full details
    - Algorithm types and their parameters
    - Creation and modification timestamps
    - Usage statistics if available
    
    Use this endpoint to:
    - Display available algorithms in UI
    - Select algorithms for device assignment
    - Review existing algorithm configurations
    """
    return await algorithms_services.get_algorithms_service(session)

@router.get("/{algorithm_id}", status_code=status.HTTP_200_OK, response_model=AlgorithmResponse)
async def get_algorithm(algorithm_id: uuid.UUID, session: SessionDependency) -> Any:
    """
    Retrieve a specific consumption algorithm by its unique ID.
    
    Path Parameters:
    - **algorithm_id**: UUID of the algorithm to retrieve
    
    Returns:
    - Complete algorithm details and configuration
    - All parameters and metadata
    - Creation and modification history
    
    Raises:
    - 404: Algorithm not found
    - 400: Invalid UUID format
    """
    algorithm = await algorithms_services.get_algorithm_service(algorithm_id, session)
    if not algorithm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algorithm not found"
        )
    return algorithm

@router.put("/{algorithm_id}", status_code=status.HTTP_200_OK, response_model=AlgorithmResponse)
async def update_algorithm(algorithm_id: uuid.UUID, algorithm: AlgorithmUpdate, session: SessionDependency) -> Any:
    """
    Update an existing consumption algorithm.
    
    Modify algorithm parameters, description, or configuration.
    Only provided fields will be updated; others remain unchanged.
    
    Path Parameters:
    - **algorithm_id**: UUID of the algorithm to update
    
    Example request (partial update):
    ```json
    {
        "description": "Updated washing machine algorithm with eco mode",
        "parameters": {
            "base_consumption": 450,
            "eco_mode_consumption": 300
        }
    }
    ```
    
    Returns:
    - Updated algorithm with all current values
    - New modification timestamp
    
    Raises:
    - 404: Algorithm not found
    - 400: Invalid update data or UUID format
    """
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
    """
    Delete a consumption algorithm from the system.
    
    ⚠️ **Warning**: This action cannot be undone. Ensure the algorithm
    is not currently in use by any devices before deletion.
    
    Path Parameters:
    - **algorithm_id**: UUID of the algorithm to delete
    
    Returns:
    - Success confirmation message
    
    Raises:
    - 404: Algorithm not found
    - 400: Algorithm is in use by devices (if validation implemented)
    - 400: Invalid UUID format
    
    Before deletion, consider:
    - Check if algorithm is assigned to any devices
    - Export algorithm configuration for backup
    - Verify this is the correct algorithm to remove
    """
    success = await algorithms_services.delete_algorithm_service(algorithm_id, session)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Algorithm not found"
        )
    return {"message": "Algorithm deleted successfully"} 