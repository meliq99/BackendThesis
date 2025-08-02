"""
Default OCR configuration for server startup.
Creates default OCR settings with placeholder API key.
"""

from models.ocr_models import OCRSettings
from utils.encryption import encrypt_api_key

# Create default OCR settings with placeholder
# User must update with real API key via frontend
default_ocr_settings = OCRSettings(
    provider="gemini",
    model_name="gemini-2.5-flash",
    api_key_encrypted=encrypt_api_key("PLACEHOLDER_API_KEY_CONFIGURE_VIA_FRONTEND"),
    is_active=False,  # Not active until real API key is provided
    max_file_size_mb=20,
    supported_formats="pdf,jpg,jpeg,png"
)