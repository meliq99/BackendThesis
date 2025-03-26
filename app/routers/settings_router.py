from fastapi import APIRouter, status, Depends
from schemes.settings_schemes import Device, DeviceResponse
from typing import Any, Annotated
from utils.get_db_connection import get_session
from services import settings_service

router = APIRouter(
    prefix="/settings",
    tags=["settings"],
)
SessionDependency = Annotated[Any, Depends(get_session)]

@router.post("/devices", status_code=status.HTTP_201_CREATED, response_model=DeviceResponse)
async def create_device(device: Device, session: SessionDependency) -> Any: 
    new_device = await settings_service.create_device_service(device, session)
    return new_device
    

