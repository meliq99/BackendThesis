"""
Repository for OCR settings and configuration management.
Handles database operations for OCR configuration with encrypted API keys.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Session, select

from models.ocr_models import OCRSettings
from schemes.ocr_schemes import OCRSettingsRequest, OCRSettingsResponse, OCRStatusResponse
from utils.encryption import encrypt_api_key

def create_or_update_ocr_settings(request: OCRSettingsRequest, session: Session) -> OCRSettingsResponse:
    """
    Create or update OCR settings with encrypted API key.
    
    Args:
        request: OCR settings request
        session: Database session
        
    Returns:
        Created/updated settings (without API key)
    """
    # Deactivate existing settings
    existing_settings = session.exec(select(OCRSettings)).all()
    for setting in existing_settings:
        setting.is_active = False
        session.add(setting)
    
    # Encrypt API key
    encrypted_api_key = encrypt_api_key(request.api_key)
    
    # Create new settings
    new_settings = OCRSettings(
        provider=request.provider,
        model_name=request.model_name,
        api_key_encrypted=encrypted_api_key,
        is_active=True,
        max_file_size_mb=request.max_file_size_mb,
        supported_formats=request.supported_formats,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    session.add(new_settings)
    session.commit()
    session.refresh(new_settings)
    
    # Return response without API key
    return OCRSettingsResponse(
        id=new_settings.id,
        provider=new_settings.provider,
        model_name=new_settings.model_name,
        is_active=new_settings.is_active,
        max_file_size_mb=new_settings.max_file_size_mb,
        supported_formats=new_settings.supported_formats,
        created_at=new_settings.created_at,
        updated_at=new_settings.updated_at
    )

def get_active_ocr_settings(session: Session) -> Optional[OCRSettingsResponse]:
    """
    Get active OCR settings.
    
    Args:
        session: Database session
        
    Returns:
        Active OCR settings (without API key) or None
    """
    statement = select(OCRSettings).where(OCRSettings.is_active == True)
    settings = session.exec(statement).first()
    
    if not settings:
        return None
    
    return OCRSettingsResponse(
        id=settings.id,
        provider=settings.provider,
        model_name=settings.model_name,
        is_active=settings.is_active,
        max_file_size_mb=settings.max_file_size_mb,
        supported_formats=settings.supported_formats,
        created_at=settings.created_at,
        updated_at=settings.updated_at
    )

def get_ocr_status(session: Session) -> OCRStatusResponse:
    """
    Get OCR service status and capabilities.
    
    Args:
        session: Database session
        
    Returns:
        OCR status information
    """
    active_settings = get_active_ocr_settings(session)
    
    if not active_settings:
        return OCRStatusResponse(
            is_configured=False,
            active_provider=None,
            active_model=None,
            supported_formats=[],
            max_file_size_mb=0,
            last_check=datetime.now().isoformat()
        )
    
    supported_formats = active_settings.supported_formats.split(',') if active_settings.supported_formats else []
    
    return OCRStatusResponse(
        is_configured=True,
        active_provider=active_settings.provider,
        active_model=active_settings.model_name,
        supported_formats=supported_formats,
        max_file_size_mb=active_settings.max_file_size_mb,
        last_check=datetime.now().isoformat()
    )