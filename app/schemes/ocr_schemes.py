"""
Schemas for OCR functionality including device data extraction from energy labels.
Defines request/response structures for document processing and device creation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID

class OCRSettingsRequest(BaseModel):
    """Request to update OCR settings."""
    
    model_config = {"protected_namespaces": ()}
    
    provider: str = Field(default="gemini", description="OCR provider")
    model_name: str = Field(default="gemini-2.5-flash", description="Model to use")
    api_key: str = Field(description="API key (will be encrypted before storage)")
    max_file_size_mb: int = Field(default=20, description="Maximum file size in MB")
    supported_formats: str = Field(default="pdf,jpg,jpeg,png", description="Supported file formats")

class OCRSettingsResponse(BaseModel):
    """Response with OCR settings (without API key)."""
    
    model_config = {"protected_namespaces": ()}
    
    id: UUID
    provider: str
    model_name: str
    is_active: bool
    max_file_size_mb: int
    supported_formats: str
    created_at: Optional[str]
    updated_at: Optional[str]
    # Note: api_key is never returned for security

class DeviceExtractionRequest(BaseModel):
    """Request to extract device data from an energy label document."""
    
    file_data: str = Field(description="Base64 encoded file data")
    file_type: str = Field(description="File MIME type (application/pdf, image/jpeg, etc.)")
    filename: Optional[str] = Field(default=None, description="Original filename")
    extract_language: str = Field(default="es", description="Language for extraction (es, en, etc.)")

# Pydantic models for structured device extraction
class EnergyConsumption(BaseModel):
    """Energy consumption information extracted from label."""
    
    annual_kwh: Optional[float] = Field(default=None, description="Annual consumption in kWh")
    daily_kwh: Optional[float] = Field(default=None, description="Daily consumption in kWh")
    power_watts: Optional[float] = Field(default=None, description="Power consumption in watts")
    energy_class: Optional[str] = Field(default=None, description="Energy efficiency class (A+, A, B, etc.)")

class DeviceSpecifications(BaseModel):
    """Device specifications extracted from label."""
    
    brand: Optional[str] = Field(default=None, description="Device brand/manufacturer")
    model: Optional[str] = Field(default=None, description="Device model number")
    device_type: Optional[str] = Field(default=None, description="Type of device (refrigerator, TV, etc.)")
    capacity: Optional[str] = Field(default=None, description="Device capacity (liters, inches, etc.)")
    features: List[str] = Field(default=[], description="Special features or characteristics")

class ExtractedDeviceData(BaseModel):
    """Complete device data extracted from energy label."""
    
    device_name: str = Field(description="Suggested device name")
    device_type: str = Field(description="Device category for algorithm selection")
    energy_consumption: EnergyConsumption = Field(description="Energy consumption data")
    specifications: DeviceSpecifications = Field(description="Device specifications")
    suggested_algorithm: str = Field(description="Suggested algorithm type based on device")
    confidence_score: float = Field(description="Confidence in extraction accuracy (0-1)")
    extraction_notes: List[str] = Field(default=[], description="Notes about the extraction process")

class DeviceExtractionResponse(BaseModel):
    """Response with extracted device data ready for device creation."""
    
    success: bool = Field(description="Whether extraction was successful")
    extracted_data: Optional[ExtractedDeviceData] = Field(default=None, description="Extracted device data")
    error_message: Optional[str] = Field(default=None, description="Error message if extraction failed")
    processing_time_seconds: float = Field(description="Time taken for processing")
    
    # Data ready for device creation
    device_creation_data: Optional["DeviceCreationData"] = Field(default=None, description="Ready-to-use device data")

class DeviceCreationData(BaseModel):
    """Device data formatted for direct device creation."""
    
    name: str = Field(description="Device name")
    description: str = Field(description="Device description")
    consumption_value: float = Field(description="Base consumption in watts")
    peak_consumption: Optional[float] = Field(default=None, description="Peak consumption in watts")
    cycle_duration: Optional[int] = Field(default=10, description="Cycle duration for algorithms")
    on_duration: Optional[int] = Field(default=5, description="On duration for algorithms")
    icon: Optional[str] = Field(default=None, description="Device icon identifier")
    suggested_algorithm_type: str = Field(description="Recommended algorithm type")

class OCRStatusResponse(BaseModel):
    """OCR service status and capabilities."""
    
    is_configured: bool = Field(description="Whether OCR is properly configured")
    active_provider: Optional[str] = Field(default=None, description="Currently active provider")
    active_model: Optional[str] = Field(default=None, description="Currently active model")
    supported_formats: List[str] = Field(description="Supported file formats")
    max_file_size_mb: int = Field(description="Maximum file size")
    last_check: Optional[str] = Field(default=None, description="Last configuration check")