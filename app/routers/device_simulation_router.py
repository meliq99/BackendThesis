from fastapi import APIRouter, status, Depends
from schemes.device_simulation_schemes import DeviceSimulation, DeviceSimulationResponse
from typing import Any, Annotated
from utils.get_db_connection import get_session
from services import device_simulation_service
import uuid

router = APIRouter(
    prefix="/device-simulation",
    tags=["device-simulation"],
)
SessionDependency = Annotated[Any, Depends(get_session)]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DeviceSimulationResponse)
async def create_device_simulation(device_simulation: DeviceSimulation, session: SessionDependency) -> Any:
    new_device_simulation = await device_simulation_service.create_device_simulation_service(device_simulation, session)
    return new_device_simulation

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[DeviceSimulationResponse])
async def get_device_simulations(electric_meter_id: uuid.UUID, session: SessionDependency) -> Any:
    return await device_simulation_service.get_device_simulations_service(electric_meter_id, session)

@router.delete("/{device_simulation_id}", status_code=status.HTTP_200_OK)
async def delete_device_simulation(device_simulation_id: uuid.UUID, session: SessionDependency) -> Any:
    return await device_simulation_service.delete_device_simulation_service(device_simulation_id, session)

@router.put("/{device_simulation_id}", status_code=status.HTTP_200_OK, response_model=DeviceSimulationResponse)
async def update_device_simulation(device_simulation_id: uuid.UUID, device_simulation: DeviceSimulation, session: SessionDependency) -> Any:
    return await device_simulation_service.update_device_simulation_service(device_simulation_id, device_simulation, session)
