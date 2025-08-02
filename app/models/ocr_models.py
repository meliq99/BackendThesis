"""
Models for OCR settings and configuration.
Stores encrypted API keys and model configurations for document processing.
"""

from sqlmodel import Field, SQLModel
import uuid
from typing import Optional

class OCRSettings(SQLModel, table=True):
    """OCR configuration settings with encrypted API key storage."""
    
    # Disable protected namespace warnings for this model
    model_config = {"protected_namespaces": ()}
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    provider: str = Field(default="gemini", description="OCR provider (gemini, etc.)")
    model_name: str = Field(default="gemini-2.5-flash", description="Model to use for OCR")
    api_key_encrypted: str = Field(description="Encrypted API key")
    is_active: bool = Field(default=True, description="Whether this configuration is active")
    max_file_size_mb: int = Field(default=20, description="Maximum file size in MB")
    supported_formats: str = Field(default="pdf,jpg,jpeg,png", description="Comma-separated supported formats")
    
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)