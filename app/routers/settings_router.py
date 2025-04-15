from fastapi import APIRouter, status, Depends
from schemes.settings_schemes import Device, DeviceResponse, Settings
from typing import Any, Annotated
from utils.get_db_connection import get_session
from services import settings_service
import uuid

router = APIRouter(
    prefix="/settings",
    tags=["settings"],
)
SessionDependency = Annotated[Any, Depends(get_session)]

@router.post("/devices", status_code=status.HTTP_201_CREATED, response_model=DeviceResponse)
async def create_device(device: Device, session: SessionDependency) -> Any: 
    new_device = await settings_service.create_device_service(device, session)
    return new_device
    

@router.get("/", status_code=status.HTTP_200_OK, response_model=Settings)
async def get_settings(session: SessionDependency) -> Any:
    return await settings_service.get_settings_service(session)

@router.delete("/devices/{device_id}", status_code=status.HTTP_200_OK)
async def delete_device(device_id: uuid.UUID, session: SessionDependency) -> Any:
    return await settings_service.delete_device_service(device_id, session)
    

