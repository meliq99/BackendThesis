"""
OCR service for extracting device data from energy labels using Gemini API.
Handles document processing and structured data extraction.
"""

import os
import time
import base64
import logging
from typing import Optional, Tuple
from sqlmodel import Session, select

from models.ocr_models import OCRSettings
from schemes.ocr_schemes import (
    DeviceExtractionRequest, 
    DeviceExtractionResponse, 
    ExtractedDeviceData,
    DeviceCreationData,
    EnergyConsumption,
    DeviceSpecifications
)
from utils.encryption import decrypt_api_key

# Import Gemini API
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    types = None

logger = logging.getLogger(__name__)

class OCRService:
    """Service for handling OCR operations with Gemini API."""
    
    def __init__(self):
        self.client = None
        self.current_settings = None
    
    def _get_active_settings(self, session: Session) -> Optional[OCRSettings]:
        """Get active OCR settings from database."""
        statement = select(OCRSettings).where(OCRSettings.is_active == True)
        return session.exec(statement).first()
    
    def _initialize_client(self, session: Session) -> bool:
        """Initialize Gemini client with current settings."""
        if not GEMINI_AVAILABLE:
            logger.error("Gemini API not available. Install with: pip install google-genai")
            return False
        
        settings = self._get_active_settings(session)
        if not settings:
            logger.error("No active OCR settings found")
            return False
        
        try:
            # Decrypt API key
            api_key = decrypt_api_key(settings.api_key_encrypted)
            
            # Initialize client
            os.environ["GEMINI_API_KEY"] = api_key
            self.client = genai.Client()
            self.current_settings = settings
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            return False
    
    def extract_device_data(self, request: DeviceExtractionRequest, session: Session) -> DeviceExtractionResponse:
        """
        Extract device data from energy label using Gemini OCR.
        
        Args:
            request: Extraction request with file data
            session: Database session
            
        Returns:
            Extracted device data or error response
        """
        start_time = time.time()
        
        try:
            # Initialize client if needed
            if not self.client and not self._initialize_client(session):
                return DeviceExtractionResponse(
                    success=False,
                    error_message="OCR service not properly configured",
                    processing_time_seconds=time.time() - start_time
                )
            
            # Decode file data
            try:
                file_bytes = base64.b64decode(request.file_data)
            except Exception as e:
                return DeviceExtractionResponse(
                    success=False,
                    error_message=f"Invalid file data: {e}",
                    processing_time_seconds=time.time() - start_time
                )
            
            # Create structured prompt for device extraction
            extraction_prompt = self._create_extraction_prompt(request.extract_language)
            
            # Process document with Gemini
            try:
                response = self.client.models.generate_content(
                    model=self.current_settings.model_name,
                    contents=[
                        types.Part.from_bytes(
                            data=file_bytes,
                            mime_type=request.file_type,
                        ),
                        extraction_prompt
                    ],
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": ExtractedDeviceData,
                    }
                )
                
                # Parse the structured response
                extracted_data: ExtractedDeviceData = response.parsed
                
                if not extracted_data:
                    return DeviceExtractionResponse(
                        success=False,
                        error_message="Failed to parse extracted data",
                        processing_time_seconds=time.time() - start_time
                    )
                
                # Convert to device creation format
                device_creation_data = self._convert_to_device_creation_data(extracted_data)
                
                return DeviceExtractionResponse(
                    success=True,
                    extracted_data=extracted_data,
                    device_creation_data=device_creation_data,
                    processing_time_seconds=time.time() - start_time
                )
                
            except Exception as e:
                logger.error(f"Gemini API error: {e}")
                return DeviceExtractionResponse(
                    success=False,
                    error_message=f"OCR processing failed: {e}",
                    processing_time_seconds=time.time() - start_time
                )
                
        except Exception as e:
            logger.error(f"Unexpected error in OCR service: {e}")
            return DeviceExtractionResponse(
                success=False,
                error_message=f"Unexpected error: {e}",
                processing_time_seconds=time.time() - start_time
            )
    
    def _create_extraction_prompt(self, language: str) -> str:
        """Create prompt for structured device data extraction."""
        
        if language.lower() == "es":
            return """
Analiza esta etiqueta energética y extrae la información del dispositivo de forma estructurada.

Extrae la siguiente información:
1. Nombre del dispositivo (marca + modelo + tipo)
2. Tipo de dispositivo (refrigerador, TV, lavadora, etc.)
3. Consumo energético:
   - Consumo anual en kWh si está disponible
   - Potencia en watts si está disponible
   - Clase energética (A+++, A++, A+, A, B, C, D, E, F, G)
4. Especificaciones:
   - Marca/fabricante
   - Número de modelo
   - Capacidad (litros, pulgadas, etc.)
   - Características especiales
5. Algoritmo sugerido basado en el tipo de dispositivo:
   - "cyclic" para refrigeradores, aires acondicionados
   - "schedule" para TVs, equipos de entretenimiento
   - "constant" para routers, equipos siempre encendidos
   - "active" para dispositivos de uso intermitente

Proporciona un puntaje de confianza del 0 al 1 basado en qué tan clara es la información en la etiqueta.

Si no puedes extraer algún dato, márcalo como null o lista vacía según corresponda.
            """
        else:
            return """
Analyze this energy label and extract device information in a structured format.

Extract the following information:
1. Device name (brand + model + type)
2. Device type (refrigerator, TV, washing machine, etc.)
3. Energy consumption:
   - Annual consumption in kWh if available
   - Power in watts if available
   - Energy efficiency class (A+++, A++, A+, A, B, C, D, E, F, G)
4. Specifications:
   - Brand/manufacturer
   - Model number
   - Capacity (liters, inches, etc.)
   - Special features
5. Suggested algorithm based on device type:
   - "cyclic" for refrigerators, air conditioners
   - "schedule" for TVs, entertainment equipment
   - "constant" for routers, always-on equipment
   - "active" for intermittent-use devices

Provide a confidence score from 0 to 1 based on how clear the information is on the label.

If you cannot extract some data, mark it as null or empty list as appropriate.
            """
    
    def _convert_to_device_creation_data(self, extracted_data: ExtractedDeviceData) -> DeviceCreationData:
        """Convert extracted data to device creation format."""
        
        # Calculate base consumption in watts
        consumption_watts = self._calculate_consumption_watts(extracted_data.energy_consumption)
        
        # Calculate peak consumption (estimate 20-50% higher than base)
        peak_consumption = self._estimate_peak_consumption(consumption_watts, extracted_data.device_type)
        
        # Create description
        description = self._create_device_description(extracted_data)
        
        # Determine icon based on device type
        icon = self._get_device_icon(extracted_data.device_type)
        
        return DeviceCreationData(
            name=extracted_data.device_name,
            description=description,
            consumption_value=consumption_watts,
            peak_consumption=peak_consumption,
            cycle_duration=self._get_default_cycle_duration(extracted_data.suggested_algorithm),
            on_duration=self._get_default_on_duration(extracted_data.suggested_algorithm),
            icon=icon,
            suggested_algorithm_type=extracted_data.suggested_algorithm
        )
    
    def _calculate_consumption_watts(self, energy_consumption: EnergyConsumption) -> float:
        """Calculate base consumption in watts from energy data."""
        
        # Priority: direct watts > daily kWh > annual kWh
        if energy_consumption.power_watts:
            return float(energy_consumption.power_watts)
        
        if energy_consumption.daily_kwh:
            # Convert daily kWh to average watts: (kWh * 1000) / 24 hours
            return (float(energy_consumption.daily_kwh) * 1000) / 24
        
        if energy_consumption.annual_kwh:
            # Convert annual kWh to average watts: (kWh * 1000) / (365 * 24) hours
            return (float(energy_consumption.annual_kwh) * 1000) / (365 * 24)
        
        # Default fallback based on energy class and device type
        return 50.0  # Default 50W if no data available
    
    def _estimate_peak_consumption(self, base_watts: float, device_type: str) -> float:
        """Estimate peak consumption based on device type."""
        
        device_type_lower = device_type.lower() if device_type else ""
        
        if "refrigerator" in device_type_lower or "freezer" in device_type_lower:
            return base_watts * 3.0  # Compressor startup
        elif "air" in device_type_lower or "ac" in device_type_lower:
            return base_watts * 2.5  # Compressor startup
        elif "tv" in device_type_lower or "television" in device_type_lower:
            return base_watts * 1.3  # Peak brightness
        elif "washing" in device_type_lower or "dryer" in device_type_lower:
            return base_watts * 2.0  # Motor startup
        else:
            return base_watts * 1.5  # General 50% increase
    
    def _create_device_description(self, extracted_data: ExtractedDeviceData) -> str:
        """Create device description from extracted data."""
        
        parts = []
        
        if extracted_data.specifications.brand:
            parts.append(f"Marca: {extracted_data.specifications.brand}")
        
        if extracted_data.specifications.model:
            parts.append(f"Modelo: {extracted_data.specifications.model}")
        
        if extracted_data.specifications.capacity:
            parts.append(f"Capacidad: {extracted_data.specifications.capacity}")
        
        if extracted_data.energy_consumption.energy_class:
            parts.append(f"Clase energética: {extracted_data.energy_consumption.energy_class}")
        
        if extracted_data.energy_consumption.annual_kwh:
            parts.append(f"Consumo anual: {extracted_data.energy_consumption.annual_kwh} kWh")
        
        return ". ".join(parts) if parts else f"Dispositivo {extracted_data.device_type}"
    
    def _get_device_icon(self, device_type: str) -> str:
        """Get icon identifier based on device type."""
        
        if not device_type:
            return "device"
        
        device_type_lower = device_type.lower()
        
        if "refrigerator" in device_type_lower or "fridge" in device_type_lower:
            return "refrigerator"
        elif "tv" in device_type_lower or "television" in device_type_lower:
            return "tv"
        elif "washing" in device_type_lower:
            return "washing-machine"
        elif "air" in device_type_lower or "ac" in device_type_lower:
            return "air-conditioner"
        elif "light" in device_type_lower or "lamp" in device_type_lower:
            return "lightbulb"
        elif "fan" in device_type_lower:
            return "fan"
        elif "microwave" in device_type_lower:
            return "microwave"
        elif "coffee" in device_type_lower:
            return "coffee"
        else:
            return "device"
    
    def _get_default_cycle_duration(self, algorithm_type: str) -> int:
        """Get default cycle duration based on algorithm type."""
        
        algorithm_defaults = {
            "cyclic": 10,      # 10 intervals for refrigerators
            "schedule": 24,    # 24 hours for TV schedules
            "constant": 1,     # Always on
            "active": 2        # 2 intervals for intermittent use
        }
        
        return algorithm_defaults.get(algorithm_type, 10)
    
    def _get_default_on_duration(self, algorithm_type: str) -> int:
        """Get default on duration based on algorithm type."""
        
        algorithm_defaults = {
            "cyclic": 5,       # 5 intervals on for refrigerators
            "schedule": 8,     # 8 hours on for TV
            "constant": 1,     # Always on
            "active": 1        # 1 interval on
        }
        
        return algorithm_defaults.get(algorithm_type, 5)

# Global OCR service instance
ocr_service = OCRService()