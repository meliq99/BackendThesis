"""
Examples for using the simulation parameter update endpoints.
Demonstrates how to update output units, time settings, and speed parameters.
"""

import json
from typing import Dict, Any

def simulation_parameter_examples() -> Dict[str, Any]:
    """Examples for updating simulation parameters."""
    
    return {
        "get_active_simulation": {
            "description": "Get currently active simulation with all parameters",
            "endpoint": "GET /simulations/active",
            "response_example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Home Energy Analysis",
                "start_date": "2024-01-01T00:00:00",
                "update_date": "2024-01-01T10:30:00",
                "is_active": True,
                "output_unit": "W",
                "time_unit": "seconds",
                "time_speed": 1.0,
                "simulation_start_time": None
            }
        },
        
        "update_output_unit_only": {
            "description": "Update only the output unit for MQTT publishing",
            "endpoint": "PUT /simulations/active/parameters",
            "request": {
                "output_unit": "kW"
            },
            "use_case": "Change display units without affecting time calculations",
            "real_time_effect": "MQTT messages will immediately use kW instead of W"
        },
        
        "update_time_settings": {
            "description": "Update time unit and speed for accelerated simulation",
            "endpoint": "PUT /simulations/active/parameters",
            "request": {
                "time_unit": "minutes",
                "time_speed": 60.0
            },
            "use_case": "Speed up simulation: 1 real minute = 1 simulated hour",
            "real_time_effect": "Algorithms will receive accelerated time parameters"
        },
        
        "historical_replay": {
            "description": "Set up historical data replay from specific start time",
            "endpoint": "PUT /simulations/active/parameters",
            "request": {
                "simulation_start_time": "2024-01-01T00:00:00Z",
                "time_speed": 3600.0,
                "output_unit": "W"
            },
            "use_case": "Replay January 1st data at 1 hour per second speed",
            "real_time_effect": "Simulation time starts from Jan 1st, progresses rapidly"
        },
        
        "daily_energy_analysis": {
            "description": "Configure for daily energy consumption analysis",
            "endpoint": "PUT /simulations/active/parameters",
            "request": {
                "output_unit": "kWh/day",
                "time_unit": "hours",
                "time_speed": 24.0
            },
            "use_case": "Show daily consumption, 1 real minute = 1 simulated day",
            "real_time_effect": "MQTT shows kWh/day, algorithms use hourly progression"
        },
        
        "update_specific_simulation": {
            "description": "Update a specific simulation by ID",
            "endpoint": "PUT /simulations/{simulation_id}",
            "request": {
                "name": "Updated Simulation Name",
                "output_unit": "kWh/month",
                "time_speed": 1.0
            },
            "use_case": "Update non-active simulation or rename current one"
        },
        
        "reset_to_real_time": {
            "description": "Reset simulation to real-time operation",
            "endpoint": "PUT /simulations/active/parameters",
            "request": {
                "time_unit": "seconds",
                "time_speed": 1.0,
                "simulation_start_time": None
            },
            "use_case": "Return to normal real-time monitoring",
            "real_time_effect": "Back to 1:1 time ratio, current timestamp"
        }
    }

def frontend_integration_examples() -> Dict[str, str]:
    """Frontend/JavaScript integration examples."""
    
    return {
        "get_current_settings": """
// Get current simulation settings
async function getCurrentSimulationSettings() {
    const response = await fetch('/simulations/active');
    if (response.ok) {
        const simulation = await response.json();
        return {
            id: simulation.id,
            name: simulation.name,
            outputUnit: simulation.output_unit,
            timeUnit: simulation.time_unit,
            timeSpeed: simulation.time_speed,
            startTime: simulation.simulation_start_time
        };
    }
    throw new Error('No active simulation found');
}
        """,
        
        "update_output_unit": """
// Update output unit for MQTT display
async function updateOutputUnit(newUnit) {
    const response = await fetch('/simulations/active/parameters', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            output_unit: newUnit
        })
    });
    
    if (response.ok) {
        const updated = await response.json();
        console.log(`Output unit changed to: ${updated.output_unit}`);
        return updated;
    } else {
        throw new Error('Failed to update output unit');
    }
}

// Usage
updateOutputUnit('kW');  // Switch to kilowatts
updateOutputUnit('kWh/day');  // Switch to daily energy
        """,
        
        "accelerate_simulation": """
// Speed up simulation for testing
async function accelerateSimulation(speedMultiplier) {
    const response = await fetch('/simulations/active/parameters', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            time_speed: speedMultiplier
        })
    });
    
    if (response.ok) {
        const updated = await response.json();
        console.log(`Simulation speed: ${updated.time_speed}x real-time`);
        return updated;
    } else {
        throw new Error('Failed to update simulation speed');
    }
}

// Usage examples
accelerateSimulation(60);    // 1 minute = 1 hour
accelerateSimulation(1440);  // 1 minute = 1 day
accelerateSimulation(1);     // Back to real-time
        """,
        
        "historical_replay": """
// Set up historical data replay
async function setupHistoricalReplay(startDate, speedMultiplier = 3600) {
    const response = await fetch('/simulations/active/parameters', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            simulation_start_time: startDate,
            time_speed: speedMultiplier,
            time_unit: 'seconds'
        })
    });
    
    if (response.ok) {
        const updated = await response.json();
        console.log(`Replaying from: ${updated.simulation_start_time}`);
        console.log(`Speed: ${updated.time_speed}x real-time`);
        return updated;
    } else {
        throw new Error('Failed to setup historical replay');
    }
}

// Usage
setupHistoricalReplay('2024-01-01T00:00:00Z', 3600);  // New Year replay
        """,
        
        "react_settings_component": """
// React component for simulation settings
import React, { useState, useEffect } from 'react';

function SimulationSettings() {
    const [simulation, setSimulation] = useState(null);
    const [updating, setUpdating] = useState(false);
    
    useEffect(() => {
        loadSimulationSettings();
    }, []);
    
    const loadSimulationSettings = async () => {
        try {
            const response = await fetch('/simulations/active');
            const data = await response.json();
            setSimulation(data);
        } catch (error) {
            console.error('Failed to load simulation settings:', error);
        }
    };
    
    const updateSetting = async (field, value) => {
        setUpdating(true);
        try {
            const response = await fetch('/simulations/active/parameters', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    [field]: value
                })
            });
            
            if (response.ok) {
                const updated = await response.json();
                setSimulation(updated);
            } else {
                throw new Error('Update failed');
            }
        } catch (error) {
            console.error('Failed to update setting:', error);
        } finally {
            setUpdating(false);
        }
    };
    
    if (!simulation) return <div>Loading...</div>;
    
    return (
        <div className="simulation-settings">
            <h3>Simulation Settings</h3>
            
            <div className="setting-group">
                <label>Output Unit:</label>
                <select 
                    value={simulation.output_unit}
                    onChange={(e) => updateSetting('output_unit', e.target.value)}
                    disabled={updating}
                >
                    <option value="W">Watts (W)</option>
                    <option value="kW">Kilowatts (kW)</option>
                    <option value="kWh/day">kWh per Day</option>
                    <option value="kWh/month">kWh per Month</option>
                    <option value="kWh/year">kWh per Year</option>
                </select>
            </div>
            
            <div className="setting-group">
                <label>Time Unit:</label>
                <select 
                    value={simulation.time_unit}
                    onChange={(e) => updateSetting('time_unit', e.target.value)}
                    disabled={updating}
                >
                    <option value="seconds">Seconds</option>
                    <option value="minutes">Minutes</option>
                    <option value="hours">Hours</option>
                </select>
            </div>
            
            <div className="setting-group">
                <label>Time Speed:</label>
                <input 
                    type="number" 
                    step="0.1"
                    value={simulation.time_speed}
                    onChange={(e) => updateSetting('time_speed', parseFloat(e.target.value))}
                    disabled={updating}
                />
                <small>1.0 = real-time, 60.0 = 1 min = 1 hour</small>
            </div>
            
            <div className="quick-actions">
                <button onClick={() => updateSetting('time_speed', 1)}>
                    Real-time
                </button>
                <button onClick={() => updateSetting('time_speed', 60)}>
                    1 min = 1 hour
                </button>
                <button onClick={() => updateSetting('time_speed', 1440)}>
                    1 min = 1 day
                </button>
            </div>
            
            {updating && <div className="updating">Updating...</div>}
        </div>
    );
}

export default SimulationSettings;
        """
    }

def curl_examples() -> Dict[str, str]:
    """Curl examples for testing simulation parameter endpoints."""
    
    return {
        "get_active_simulation": '''
curl -X GET "http://localhost:8000/simulations/active"
        ''',
        
        "get_supported_options": '''
curl -X GET "http://localhost:8000/simulations/supported-options"
        ''',
        
        "update_output_unit": '''
curl -X PUT "http://localhost:8000/simulations/active/parameters" \\
     -H "Content-Type: application/json" \\
     -d '{"output_unit": "kW"}'
        ''',
        
        "accelerate_simulation": '''
curl -X PUT "http://localhost:8000/simulations/active/parameters" \\
     -H "Content-Type: application/json" \\
     -d '{"time_speed": 60.0}'
        ''',
        
        "set_time_unit": '''
curl -X PUT "http://localhost:8000/simulations/active/parameters" \\
     -H "Content-Type: application/json" \\
     -d '{"time_unit": "minutes"}'
        ''',
        
        "historical_replay": '''
curl -X PUT "http://localhost:8000/simulations/active/parameters" \\
     -H "Content-Type: application/json" \\
     -d '{
         "simulation_start_time": "2024-01-01T00:00:00Z",
         "time_speed": 3600.0,
         "output_unit": "W"
     }'
        ''',
        
        "reset_to_realtime": '''
curl -X PUT "http://localhost:8000/simulations/active/parameters" \\
     -H "Content-Type: application/json" \\
     -d '{
         "time_unit": "seconds",
         "time_speed": 1.0,
         "simulation_start_time": null
     }'
        '''
    }

def workflow_examples():
    """Complete workflow examples."""
    
    print("=== Simulation Parameter Update Workflows ===")
    print()
    
    print("1. Real-time Monitoring Setup:")
    print("   GET /simulations/active  # Check current settings")
    print("   PUT /simulations/active/parameters")
    print("   {\"output_unit\": \"W\", \"time_speed\": 1.0}")
    print()
    
    print("2. Fast Testing Mode:")
    print("   PUT /simulations/active/parameters")
    print("   {\"time_speed\": 60.0, \"time_unit\": \"minutes\"}")
    print("   # 1 real minute = 1 simulated hour")
    print()
    
    print("3. Daily Energy Analysis:")
    print("   PUT /simulations/active/parameters")
    print("   {\"output_unit\": \"kWh/day\", \"time_speed\": 1440.0}")
    print("   # 1 real minute = 1 simulated day")
    print()
    
    print("4. Historical Data Replay:")
    print("   PUT /simulations/active/parameters")
    print("   {")
    print("     \"simulation_start_time\": \"2024-01-01T00:00:00Z\",")
    print("     \"time_speed\": 3600.0")
    print("   }")
    print("   # Replay January 1st at 1 hour per second")
    print()
    
    print("Benefits:")
    print("✅ Immediate effect on MQTT publishing")
    print("✅ No server restart required")
    print("✅ Flexible time and unit configurations")
    print("✅ Perfect for testing and demonstrations")
    print("✅ Historical data replay capabilities")

if __name__ == "__main__":
    # Print examples
    parameter_examples = simulation_parameter_examples()
    frontend_examples = frontend_integration_examples()
    
    print("Simulation Parameter Examples:")
    for name, example in parameter_examples.items():
        print(f"\n{name}:")
        print(f"  Description: {example['description']}")
        print(f"  Endpoint: {example['endpoint']}")
        if 'request' in example:
            print(f"  Request: {json.dumps(example['request'], indent=2)}")
        if 'use_case' in example:
            print(f"  Use Case: {example['use_case']}")
        if 'real_time_effect' in example:
            print(f"  Real-time Effect: {example['real_time_effect']}")
    
    print("\n" + "="*50)
    workflow_examples()