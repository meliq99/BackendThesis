"""
Examples of the enhanced MQTT message structure with simulation parameters.
Shows how the frontend can now receive unit and time information via MQTT.
"""

import json
from typing import Dict, Any

def mqtt_message_examples() -> Dict[str, Any]:
    """Examples of MQTT messages with simulation parameters."""
    
    return {
        "basic_real_time_message": {
            "description": "Standard real-time consumption message",
            "mqtt_message": {
                "value": 42.5,
                "unit": "W",
                "time_unit": "seconds",
                "time_speed": 1.0,
                "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
                "timestamp": 1704067200
            },
            "interpretation": {
                "consumption": "42.5 Watts current consumption",
                "time_mode": "Real-time (1:1 ratio)",
                "algorithm_timing": "Algorithms use second-based intervals"
            }
        },
        
        "accelerated_simulation_message": {
            "description": "Fast simulation with different units",
            "mqtt_message": {
                "value": 1.02,
                "unit": "kWh/day",
                "time_unit": "hours",
                "time_speed": 24.0,
                "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
                "timestamp": 1704153600
            },
            "interpretation": {
                "consumption": "1.02 kWh per day projected consumption",
                "time_mode": "Accelerated: 1 real minute = 1 simulated day",
                "algorithm_timing": "Algorithms use hour-based intervals"
            }
        },
        
        "historical_replay_message": {
            "description": "Historical data replay at high speed",
            "mqtt_message": {
                "value": 156.8,
                "unit": "W",
                "time_unit": "seconds",
                "time_speed": 3600.0,
                "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
                "timestamp": 1704067200
            },
            "interpretation": {
                "consumption": "156.8 Watts historical consumption",
                "time_mode": "Historical replay: 1 real second = 1 simulated hour",
                "algorithm_timing": "Algorithms use second-based intervals",
                "note": "Timestamp represents historical simulation time"
            }
        },
        
        "energy_analysis_message": {
            "description": "Monthly energy analysis mode",
            "mqtt_message": {
                "value": 45.2,
                "unit": "kWh/month",
                "time_unit": "minutes",
                "time_speed": 60.0,
                "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
                "timestamp": 1704067200
            },
            "interpretation": {
                "consumption": "45.2 kWh per month projected consumption",
                "time_mode": "Fast analysis: 1 real minute = 1 simulated hour",
                "algorithm_timing": "Algorithms use minute-based intervals"
            }
        }
    }

def frontend_integration_examples() -> Dict[str, str]:
    """Frontend integration examples for handling MQTT messages."""
    
    return {
        "javascript_mqtt_handler": """
// JavaScript MQTT message handler
function handleMQTTMessage(message) {
    const data = JSON.parse(message);
    
    // Extract consumption value and metadata
    const {
        value,
        unit,
        time_unit,
        time_speed,
        simulation_id,
        timestamp
    } = data;
    
    // Update consumption display
    updateConsumptionDisplay(value, unit);
    
    // Update simulation info
    updateSimulationInfo({
        timeUnit: time_unit,
        timeSpeed: time_speed,
        simulationId: simulation_id,
        lastUpdate: new Date(timestamp * 1000)
    });
    
    // Show time mode indicator
    updateTimeModeIndicator(time_speed, time_unit);
}

function updateConsumptionDisplay(value, unit) {
    const displayElement = document.getElementById('consumption-value');
    const unitElement = document.getElementById('consumption-unit');
    
    displayElement.textContent = value.toFixed(1);
    unitElement.textContent = unit;
    
    // Add unit-specific styling
    displayElement.className = getUnitClass(unit);
}

function updateSimulationInfo(info) {
    const infoElement = document.getElementById('simulation-info');
    
    // Show time mode
    const timeMode = getTimeModeDescription(info.timeSpeed);
    infoElement.innerHTML = `
        <div>Time Mode: ${timeMode}</div>
        <div>Algorithm Timing: ${info.timeUnit}</div>
        <div>Simulation ID: ${info.simulationId}</div>
        <div>Last Update: ${info.lastUpdate.toLocaleTimeString()}</div>
    `;
}

function getTimeModeDescription(timeSpeed) {
    if (timeSpeed === 1.0) {
        return "Real-time";
    } else if (timeSpeed > 1.0) {
        return `${timeSpeed}x Accelerated`;
    } else {
        return `${1/timeSpeed}x Slow Motion`;
    }
}

function getUnitClass(unit) {
    const unitClasses = {
        'W': 'power-watts',
        'kW': 'power-kilowatts',
        'kWh/day': 'energy-daily',
        'kWh/month': 'energy-monthly',
        'kWh/year': 'energy-yearly'
    };
    return unitClasses[unit] || 'default-unit';
}
        """,
        
        "react_mqtt_component": """
// React component for MQTT data display
import React, { useState, useEffect } from 'react';

function ConsumptionDisplay({ mqttClient }) {
    const [consumptionData, setConsumptionData] = useState(null);
    const [simulationInfo, setSimulationInfo] = useState(null);
    
    useEffect(() => {
        if (mqttClient) {
            mqttClient.on('message', handleMQTTMessage);
        }
        
        return () => {
            if (mqttClient) {
                mqttClient.off('message', handleMQTTMessage);
            }
        };
    }, [mqttClient]);
    
    const handleMQTTMessage = (topic, message) => {
        try {
            const data = JSON.parse(message.toString());
            
            setConsumptionData({
                value: data.value,
                unit: data.unit,
                timestamp: new Date(data.timestamp * 1000)
            });
            
            setSimulationInfo({
                timeUnit: data.time_unit,
                timeSpeed: data.time_speed,
                simulationId: data.simulation_id,
                timeMode: getTimeModeDescription(data.time_speed)
            });
        } catch (error) {
            console.error('Error parsing MQTT message:', error);
        }
    };
    
    const getTimeModeDescription = (timeSpeed) => {
        if (timeSpeed === 1.0) return "Real-time";
        if (timeSpeed > 1.0) return `${timeSpeed}x Accelerated`;
        return `${(1/timeSpeed).toFixed(1)}x Slow Motion`;
    };
    
    const getUnitColor = (unit) => {
        const colors = {
            'W': '#2196F3',
            'kW': '#FF9800',
            'kWh/day': '#4CAF50',
            'kWh/month': '#9C27B0',
            'kWh/year': '#F44336'
        };
        return colors[unit] || '#666';
    };
    
    if (!consumptionData) {
        return <div>Waiting for MQTT data...</div>;
    }
    
    return (
        <div className="consumption-display">
            <div className="main-value">
                <span 
                    className="value"
                    style={{ color: getUnitColor(consumptionData.unit) }}
                >
                    {consumptionData.value.toFixed(1)}
                </span>
                <span className="unit">{consumptionData.unit}</span>
            </div>
            
            {simulationInfo && (
                <div className="simulation-info">
                    <div className="time-mode">
                        <strong>Mode:</strong> {simulationInfo.timeMode}
                    </div>
                    <div className="algorithm-timing">
                        <strong>Algorithm Timing:</strong> {simulationInfo.timeUnit}
                    </div>
                    <div className="last-update">
                        <strong>Last Update:</strong> {consumptionData.timestamp.toLocaleTimeString()}
                    </div>
                </div>
            )}
            
            <div className="indicators">
                {simulationInfo?.timeSpeed !== 1.0 && (
                    <div className="speed-indicator">
                        🚀 {simulationInfo.timeMode}
                    </div>
                )}
                {consumptionData.unit !== 'W' && (
                    <div className="unit-indicator">
                        📊 {consumptionData.unit} Mode
                    </div>
                )}
            </div>
        </div>
    );
}

export default ConsumptionDisplay;
        """,
        
        "mqtt_topic_subscription": """
// MQTT topic subscription and configuration
const mqtt = require('mqtt');

// Connect to MQTT broker
const client = mqtt.connect('mqtt://localhost:1883');

client.on('connect', () => {
    console.log('Connected to MQTT broker');
    
    // Subscribe to consumption data topic
    client.subscribe('consumption/data', (err) => {
        if (err) {
            console.error('Failed to subscribe:', err);
        } else {
            console.log('Subscribed to consumption data');
        }
    });
});

client.on('message', (topic, message) => {
    if (topic === 'consumption/data') {
        try {
            const data = JSON.parse(message.toString());
            
            // Handle the enhanced message structure
            console.log('Consumption Data:', {
                value: data.value,
                unit: data.unit,
                timeMode: data.time_speed === 1.0 ? 'Real-time' : `${data.time_speed}x`,
                algorithmTiming: data.time_unit,
                simulationId: data.simulation_id,
                timestamp: new Date(data.timestamp * 1000)
            });
            
            // Process the data based on unit type
            processConsumptionData(data);
            
        } catch (error) {
            console.error('Error parsing MQTT message:', error);
        }
    }
});

function processConsumptionData(data) {
    // Handle different unit types
    switch (data.unit) {
        case 'W':
        case 'kW':
            // Handle power consumption
            updatePowerDisplay(data.value, data.unit);
            break;
            
        case 'kWh/day':
        case 'kWh/month':
        case 'kWh/year':
            // Handle energy consumption projections
            updateEnergyProjection(data.value, data.unit);
            break;
            
        default:
            console.warn('Unknown unit type:', data.unit);
    }
    
    // Update time mode indicator
    updateTimeMode(data.time_speed, data.time_unit);
}
        """
    }

def api_examples() -> Dict[str, str]:
    """API examples for getting MQTT structure information."""
    
    return {
        "get_current_parameters": '''
curl -X GET "http://localhost:8000/current-parameters"
        ''',
        
        "get_sample_mqtt_message": '''
curl -X GET "http://localhost:8000/sample-mqtt-message"
        ''',
        
        "javascript_api_fetch": '''
// Fetch current simulation parameters
async function getCurrentParameters() {
    const response = await fetch('/current-parameters');
    const data = await response.json();
    
    console.log('Current simulation settings:', {
        outputUnit: data.output_unit,
        timeUnit: data.time_unit,
        timeSpeed: data.time_speed,
        simulationId: data.simulation_id
    });
    
    return data;
}

// Get sample MQTT message structure
async function getSampleMQTTStructure() {
    const response = await fetch('/sample-mqtt-message');
    const data = await response.json();
    
    console.log('MQTT message structure:', data.mqtt_message_structure);
    console.log('Field descriptions:', data.field_descriptions);
    
    return data;
}
        '''
    }

def message_evolution_example():
    """Show how messages change when parameters are updated."""
    
    print("=== MQTT Message Evolution Example ===")
    print()
    
    print("1. Initial Real-time Message:")
    print(json.dumps({
        "value": 42.5,
        "unit": "W",
        "time_unit": "seconds",
        "time_speed": 1.0,
        "simulation_id": "123...",
        "timestamp": 1704067200
    }, indent=2))
    print()
    
    print("2. After changing output unit to kW:")
    print("   PUT /simulations/active/parameters {\"output_unit\": \"kW\"}")
    print(json.dumps({
        "value": 0.0425,  # Converted from 42.5W to kW
        "unit": "kW",
        "time_unit": "seconds",
        "time_speed": 1.0,
        "simulation_id": "123...",
        "timestamp": 1704067202
    }, indent=2))
    print()
    
    print("3. After accelerating simulation:")
    print("   PUT /simulations/active/parameters {\"time_speed\": 60.0}")
    print(json.dumps({
        "value": 0.0425,
        "unit": "kW",
        "time_unit": "seconds",
        "time_speed": 60.0,  # Now 60x faster
        "simulation_id": "123...",
        "timestamp": 1704067800  # Time progresses faster
    }, indent=2))
    print()
    
    print("4. Switch to daily energy analysis:")
    print("   PUT /simulations/active/parameters {\"output_unit\": \"kWh/day\", \"time_unit\": \"hours\"}")
    print(json.dumps({
        "value": 1.02,  # Daily energy projection
        "unit": "kWh/day",
        "time_unit": "hours",
        "time_speed": 60.0,
        "simulation_id": "123...",
        "timestamp": 1704068400
    }, indent=2))
    print()
    
    print("Benefits:")
    print("✅ Frontend always knows current unit without guessing")
    print("✅ Time mode is clearly indicated in each message")
    print("✅ Simulation ID helps track which configuration is active")
    print("✅ Timestamp works for both real-time and historical replay")
    print("✅ Parameters change immediately when updated via API")

if __name__ == "__main__":
    # Print examples
    mqtt_examples = mqtt_message_examples()
    
    print("Enhanced MQTT Message Examples:")
    for name, example in mqtt_examples.items():
        print(f"\n{name}:")
        print(f"  Description: {example['description']}")
        print(f"  MQTT Message: {json.dumps(example['mqtt_message'], indent=2)}")
        if 'interpretation' in example:
            print(f"  Interpretation:")
            for key, value in example['interpretation'].items():
                print(f"    {key}: {value}")
    
    print("\n" + "="*50)
    message_evolution_example()