"""
Router for OCR functionality including device data extraction from energy labels.
Provides endpoints for OCR configuration and document processing.
"""

from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session
import base64
import time

from utils.get_db_connection import get_session
from schemes.ocr_schemes import (
    OCRSettingsRequest,
    OCRSettingsResponse, 
    DeviceExtractionRequest,
    DeviceExtractionResponse,
    OCRStatusResponse
)
from services.ocr_service import ocr_service
from repository.ocr_repository import (
    create_or_update_ocr_settings,
    get_active_ocr_settings,
    get_ocr_status
)

router = APIRouter(prefix="/ocr", tags=["OCR"])

SessionDependency = Annotated[Session, Depends(get_session)]

@router.post("/settings", response_model=OCRSettingsResponse)
async def update_ocr_settings(
    request: OCRSettingsRequest,
    session: SessionDependency
) -> Any:
    """
    Update OCR settings including API key configuration.
    
    The API key will be encrypted before storage and never returned in responses.
    
    Example request:
    ```json
    {
        "provider": "gemini",
        "model_name": "gemini-2.5-flash",
        "api_key": "your-gemini-api-key",
        "max_file_size_mb": 20,
        "supported_formats": "pdf,jpg,jpeg,png"
    }
    ```
    
    Returns:
    - OCR configuration (without API key)
    - Success/error status
    """
    try:
        settings = create_or_update_ocr_settings(request, session)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update OCR settings: {e}")

@router.get("/settings", response_model=OCRSettingsResponse)
async def get_ocr_settings(session: SessionDependency) -> Any:
    """
    Get current OCR settings.
    
    Returns current configuration without the API key for security.
    """
    try:
        settings = get_active_ocr_settings(session)
        if not settings:
            raise HTTPException(status_code=404, detail="No OCR settings configured")
        return settings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get OCR settings: {e}")

@router.get("/status", response_model=OCRStatusResponse)
async def get_ocr_status_endpoint(session: SessionDependency) -> Any:
    """
    Get OCR service status and capabilities.
    
    Returns:
    - Configuration status
    - Active provider and model
    - Supported formats and limits
    """
    try:
        return get_ocr_status(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get OCR status: {e}")

@router.post("/extract-device", response_model=DeviceExtractionResponse)
async def extract_device_data(
    request: DeviceExtractionRequest,
    session: SessionDependency
) -> Any:
    """
    Extract device data from energy label using OCR.
    
    Processes energy label images/PDFs and returns structured device data
    ready for device creation.
    
    Example request:
    ```json
    {
        "file_data": "base64-encoded-file-data",
        "file_type": "application/pdf",
        "filename": "energy_label.pdf",
        "extract_language": "es"
    }
    ```
    
    Returns:
    - Extracted device information
    - Device creation data ready for use
    - Processing statistics and confidence scores
    """
    try:
        # Validate file size (approximate check on base64 data)
        file_size_mb = len(request.file_data) * 0.75 / (1024 * 1024)  # Base64 overhead
        
        # Get current settings to check limits
        settings = get_active_ocr_settings(session)
        if not settings:
            raise HTTPException(status_code=503, detail="OCR service not configured")
        
        if file_size_mb > settings.max_file_size_mb:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
            )
        
        # Validate file type
        supported_types = {
            "application/pdf": "pdf",
            "image/jpeg": "jpg", 
            "image/jpg": "jpg",
            "image/png": "png"
        }
        
        if request.file_type not in supported_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {request.file_type}. Supported: {list(supported_types.keys())}"
            )
        
        # Process with OCR service
        result = ocr_service.extract_device_data(request, session)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {e}")

@router.post("/extract-device-upload", response_model=DeviceExtractionResponse)
async def extract_device_data_upload(
    session: SessionDependency,
    file: UploadFile = File(...),
    extract_language: str = Form(default="es")
) -> Any:
    """
    Extract device data from uploaded energy label file.
    
    Alternative endpoint that accepts file uploads directly instead of base64 data.
    More convenient for frontend file upload components.
    
    Form parameters:
    - file: Energy label file (PDF, JPG, PNG)
    - extract_language: Language for extraction (default: "es")
    
    Returns same structure as /extract-device endpoint.
    """
    try:
        # Read and encode file
        file_content = await file.read()
        file_data_b64 = base64.b64encode(file_content).decode()
        
        # Create extraction request
        extraction_request = DeviceExtractionRequest(
            file_data=file_data_b64,
            file_type=file.content_type or "application/octet-stream",
            filename=file.filename,
            extract_language=extract_language
        )
        
        # Process with the main extraction logic
        return await extract_device_data(extraction_request, session)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload processing failed: {e}")

@router.post("/test-connection")
async def test_ocr_connection(session: SessionDependency) -> Any:
    """
    Test OCR service connection and configuration.
    
    Validates that:
    - OCR settings are configured
    - API key is valid
    - Service is reachable
    
    Returns test results and any configuration issues.
    """
    try:
        # Check if settings exist
        settings = get_active_ocr_settings(session)
        if not settings:
            return {
                "success": False,
                "message": "No OCR settings configured",
                "details": "Please configure OCR settings first"
            }
        
        # Test with a simple request (you could add a minimal test here)
        # For now, just verify we can initialize the service
        if ocr_service._initialize_client(session):
            return {
                "success": True,
                "message": "OCR service connection successful",
                "provider": settings.provider,
                "model": settings.model_name
            }
        else:
            return {
                "success": False,
                "message": "OCR service connection failed",
                "details": "Check API key and network connectivity"
            }
            
    except Exception as e:
        return {
            "success": False,
            "message": "OCR connection test failed",
            "details": str(e)
        }

@router.get("/supported-formats")
async def get_supported_formats() -> Any:
    """
    Get supported file formats and processing capabilities.
    
    Returns:
    - Supported MIME types
    - File size limits
    - Processing capabilities
    """
    return {
        "supported_formats": {
            "pdf": {
                "mime_types": ["application/pdf"],
                "description": "PDF documents up to 1000 pages",
                "max_size_mb": 20,
                "features": ["text", "images", "charts", "tables"]
            },
            "images": {
                "mime_types": ["image/jpeg", "image/jpg", "image/png"],
                "description": "Image files with energy labels",
                "max_size_mb": 10,
                "features": ["text", "diagrams", "charts"]
            }
        },
        "processing_capabilities": {
            "languages": ["es", "en"],
            "max_pages": 1000,
            "structured_output": True,
            "confidence_scoring": True,
            "device_type_detection": True,
            "energy_class_recognition": True
        },
        "output_formats": {
            "device_data": "Structured device information",
            "creation_ready": "Data ready for device creation",
            "confidence_scores": "Extraction confidence metrics"
        }
    }