"""
Examples for using the OCR functionality to extract device data from energy labels.
Demonstrates the complete workflow from configuration to device creation.
"""

import json
import base64
from typing import Dict, Any

def ocr_setup_examples() -> Dict[str, Any]:
    """Examples for setting up OCR configuration."""
    
    return {
        "configure_gemini_ocr": {
            "description": "Configure OCR with Gemini API",
            "endpoint": "POST /ocr/settings",
            "request": {
                "provider": "gemini",
                "model_name": "gemini-2.5-flash",
                "api_key": "your-actual-gemini-api-key-here",
                "max_file_size_mb": 20,
                "supported_formats": "pdf,jpg,jpeg,png"
            },
            "note": "API key will be encrypted and stored securely. Never returned in responses."
        },
        
        "check_ocr_status": {
            "description": "Check OCR service status",
            "endpoint": "GET /ocr/status",
            "response_example": {
                "is_configured": True,
                "active_provider": "gemini",
                "active_model": "gemini-2.5-flash",
                "supported_formats": ["pdf", "jpg", "jpeg", "png"],
                "max_file_size_mb": 20,
                "last_check": "2024-01-01T10:00:00"
            }
        },
        
        "test_connection": {
            "description": "Test OCR service connection",
            "endpoint": "POST /ocr/test-connection",
            "response_example": {
                "success": True,
                "message": "OCR service connection successful",
                "provider": "gemini",
                "model": "gemini-2.5-flash"
            }
        }
    }

def device_extraction_examples() -> Dict[str, Any]:
    """Examples for extracting device data from energy labels."""
    
    return {
        "extract_from_base64": {
            "description": "Extract device data from base64 encoded energy label",
            "endpoint": "POST /ocr/extract-device",
            "request": {
                "file_data": "base64-encoded-pdf-or-image-data",
                "file_type": "application/pdf",
                "filename": "refrigerator_label.pdf",
                "extract_language": "es"
            },
            "response_example": {
                "success": True,
                "extracted_data": {
                    "device_name": "MABE Refrigerador RMP840FYEU1",
                    "device_type": "refrigerator",
                    "energy_consumption": {
                        "annual_kwh": 368.7,
                        "power_watts": 42.1,
                        "energy_class": "A"
                    },
                    "specifications": {
                        "brand": "MABE",
                        "model": "RMP840FYEU1",
                        "device_type": "Refrigerador sin escarcha",
                        "capacity": "391L total, 290L fresh, 101L freezer"
                    },
                    "suggested_algorithm": "cyclic",
                    "confidence_score": 0.95
                },
                "device_creation_data": {
                    "name": "MABE Refrigerador RMP840FYEU1",
                    "description": "Marca: MABE. Modelo: RMP840FYEU1. Capacidad: 391L. Clase energética: A. Consumo anual: 368.7 kWh",
                    "consumption_value": 42.1,
                    "peak_consumption": 126.3,
                    "cycle_duration": 10,
                    "on_duration": 5,
                    "icon": "refrigerator",
                    "suggested_algorithm_type": "cyclic"
                },
                "processing_time_seconds": 3.2
            }
        },
        
        "extract_from_upload": {
            "description": "Extract device data from file upload",
            "endpoint": "POST /ocr/extract-device-upload",
            "method": "multipart/form-data",
            "form_fields": {
                "file": "energy_label.pdf (binary file)",
                "extract_language": "es"
            },
            "note": "More convenient for frontend file upload components"
        }
    }

def javascript_integration_examples() -> Dict[str, str]:
    """JavaScript/frontend integration examples."""
    
    return {
        "configure_ocr": """
// Configure OCR with API key
async function configureOCR(apiKey) {
    const response = await fetch('/ocr/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            provider: 'gemini',
            model_name: 'gemini-2.5-flash',
            api_key: apiKey,
            max_file_size_mb: 20,
            supported_formats: 'pdf,jpg,jpeg,png'
        })
    });
    
    if (response.ok) {
        console.log('OCR configured successfully');
        return await response.json();
    } else {
        throw new Error('Failed to configure OCR');
    }
}
        """,
        
        "file_upload_extraction": """
// Extract device data from file upload
async function extractDeviceFromFile(file, language = 'es') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('extract_language', language);
    
    const response = await fetch('/ocr/extract-device-upload', {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        const result = await response.json();
        if (result.success) {
            return result.device_creation_data;
        } else {
            throw new Error(result.error_message);
        }
    } else {
        throw new Error('OCR extraction failed');
    }
}
        """,
        
        "react_component": """
// React component for OCR device extraction
import React, { useState } from 'react';

function DeviceExtractor() {
    const [file, setFile] = useState(null);
    const [extracting, setExtracting] = useState(false);
    const [extractedDevice, setExtractedDevice] = useState(null);
    const [error, setError] = useState(null);
    
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
        setError(null);
    };
    
    const extractDevice = async () => {
        if (!file) return;
        
        setExtracting(true);
        setError(null);
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('extract_language', 'es');
            
            const response = await fetch('/ocr/extract-device-upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                setExtractedDevice(result.device_creation_data);
            } else {
                setError(result.error_message);
            }
        } catch (err) {
            setError('Error procesando archivo: ' + err.message);
        } finally {
            setExtracting(false);
        }
    };
    
    const createDevice = async () => {
        if (!extractedDevice) return;
        
        try {
            // Use the device creation data to create a new device
            const response = await fetch('/devices', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(extractedDevice)
            });
            
            if (response.ok) {
                alert('Dispositivo creado exitosamente!');
                setExtractedDevice(null);
                setFile(null);
            } else {
                throw new Error('Error creando dispositivo');
            }
        } catch (err) {
            setError('Error creando dispositivo: ' + err.message);
        }
    };
    
    return (
        <div className="device-extractor">
            <h3>Extraer Dispositivo de Etiqueta Energética</h3>
            
            <div className="file-upload">
                <input 
                    type="file" 
                    accept=".pdf,.jpg,.jpeg,.png"
                    onChange={handleFileChange}
                />
                <button 
                    onClick={extractDevice}
                    disabled={!file || extracting}
                >
                    {extracting ? 'Procesando...' : 'Extraer Datos'}
                </button>
            </div>
            
            {error && (
                <div className="error">
                    <p>Error: {error}</p>
                </div>
            )}
            
            {extractedDevice && (
                <div className="extracted-device">
                    <h4>Dispositivo Extraído:</h4>
                    <p><strong>Nombre:</strong> {extractedDevice.name}</p>
                    <p><strong>Descripción:</strong> {extractedDevice.description}</p>
                    <p><strong>Consumo Base:</strong> {extractedDevice.consumption_value}W</p>
                    <p><strong>Consumo Pico:</strong> {extractedDevice.peak_consumption}W</p>
                    <p><strong>Algoritmo Sugerido:</strong> {extractedDevice.suggested_algorithm_type}</p>
                    
                    <button onClick={createDevice}>
                        Crear Dispositivo
                    </button>
                </div>
            )}
        </div>
    );
}

export default DeviceExtractor;
        """
    }

def curl_examples() -> Dict[str, str]:
    """Curl examples for testing OCR endpoints."""
    
    return {
        "configure_ocr": '''
curl -X POST "http://localhost:8000/ocr/settings" \\
     -H "Content-Type: application/json" \\
     -d '{
         "provider": "gemini",
         "model_name": "gemini-2.5-flash", 
         "api_key": "your-actual-api-key",
         "max_file_size_mb": 20,
         "supported_formats": "pdf,jpg,jpeg,png"
     }'
        ''',
        
        "check_status": '''
curl -X GET "http://localhost:8000/ocr/status"
        ''',
        
        "test_connection": '''
curl -X POST "http://localhost:8000/ocr/test-connection"
        ''',
        
        "upload_file": '''
curl -X POST "http://localhost:8000/ocr/extract-device-upload" \\
     -F "file=@energy_label.pdf" \\
     -F "extract_language=es"
        ''',
        
        "get_capabilities": '''
curl -X GET "http://localhost:8000/ocr/supported-formats"
        '''
    }

def workflow_example():
    """Complete workflow example."""
    
    print("=== Complete OCR Workflow Example ===")
    print()
    
    print("1. Configure OCR (one-time setup):")
    print("   POST /ocr/settings")
    print("   - Add your Gemini API key")
    print("   - Key is encrypted and stored securely")
    print()
    
    print("2. Check OCR status:")
    print("   GET /ocr/status")
    print("   - Verify configuration is active")
    print()
    
    print("3. Upload energy label:")
    print("   POST /ocr/extract-device-upload")
    print("   - Upload PDF or image file")
    print("   - Specify language (es/en)")
    print()
    
    print("4. Get structured device data:")
    print("   - Device name and specifications")
    print("   - Energy consumption in watts")
    print("   - Suggested algorithm type")
    print("   - Ready-to-use device creation data")
    print()
    
    print("5. Create device (optional):")
    print("   POST /devices")
    print("   - Use the device_creation_data directly")
    print("   - No manual data entry needed!")
    print()
    
    print("Benefits:")
    print("✅ No manual data entry")
    print("✅ Accurate consumption values")
    print("✅ Automatic algorithm selection")
    print("✅ Multi-language support")
    print("✅ Secure API key storage")

if __name__ == "__main__":
    # Print examples
    setup_examples = ocr_setup_examples()
    extraction_examples = device_extraction_examples()
    js_examples = javascript_integration_examples()
    
    print("OCR Setup Examples:")
    for name, example in setup_examples.items():
        print(f"\n{name}:")
        print(f"  Description: {example['description']}")
        print(f"  Endpoint: {example['endpoint']}")
        if 'request' in example:
            print(f"  Request: {json.dumps(example['request'], indent=2)}")
    
    print("\n" + "="*50)
    print("Device Extraction Examples:")
    for name, example in extraction_examples.items():
        print(f"\n{name}:")
        print(f"  Description: {example['description']}")
        print(f"  Endpoint: {example['endpoint']}")
    
    print("\n" + "="*50)
    workflow_example()