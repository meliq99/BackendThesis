"""
Examples and test cases for the simulation data generation API.
This demonstrates how to use the new endpoints for different scenarios.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any

def example_requests() -> Dict[str, Dict[str, Any]]:
    """Return example API requests for different use cases."""
    
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    next_week = now + timedelta(weeks=1)
    
    return {
        "daily_analysis": {
            "description": "Analyze consumption patterns for one day using simulation config",
            "endpoint": "POST /simulation-data/generate",
            "request": {
                "simulation_id": "550e8400-e29b-41d4-a716-446655440000",
                "use_current_simulation": True,
                "start_time": now.isoformat(),
                "end_time": tomorrow.isoformat(),
                "sample_interval_seconds": 3600  # Every hour
            },
            "use_case": "Real-time daily monitoring with simulation's time/unit config"
        },
        
        "fast_daily_preview": {
            "description": "See daily patterns with custom speed override",
            "endpoint": "POST /simulation-data/generate",
            "request": {
                "simulation_id": "550e8400-e29b-41d4-a716-446655440000",
                "use_current_simulation": False,
                "start_time": now.isoformat(),
                "end_time": tomorrow.isoformat(),
                "sample_interval_seconds": 60,  # Every minute
                "time_unit": "minutes",
                "time_speed": 60.0,
                "output_unit": "W"
            },
            "use_case": "Quick daily pattern analysis with custom speed"
        },
        
        "weekly_energy_analysis": {
            "description": "Weekly energy consumption analysis with custom output unit",
            "endpoint": "POST /simulation-data/generate", 
            "request": {
                "simulation_id": "550e8400-e29b-41d4-a716-446655440000",
                "use_current_simulation": False,
                "start_time": now.isoformat(),
                "end_time": next_week.isoformat(),
                "sample_interval_seconds": 21600,  # Every 6 hours
                "time_unit": "days",
                "time_speed": 7.0,
                "output_unit": "kWh/day"
            },
            "use_case": "Weekly energy planning with energy units"
        },
        
        "ultra_fast_testing": {
            "description": "Test yearly patterns in minutes",
            "endpoint": "POST /simulation-data/generate",
            "request": {
                "time_unit": "days",
                "time_speed": 365.0,
                "output_unit": "kWh/year", 
                "start_time": "2024-01-01T00:00:00",
                "end_time": "2024-12-31T23:59:59",
                "sample_interval_seconds": 86400  # Daily samples
            },
            "use_case": "Yearly consumption projection"
        },
        
        "simple_preview": {
            "description": "Simple 24-hour preview using simulation config",
            "endpoint": "POST /simulation-data/preview",
            "request": {
                "simulation_id": "550e8400-e29b-41d4-a716-446655440000",
                "duration_hours": 24.0,
                "use_current_simulation": True,
                "sample_interval_minutes": 15
            },
            "use_case": "Quick consumption preview with simulation's settings"
        },
        
        "device_specific_analysis": {
            "description": "Analyze specific devices only",
            "endpoint": "POST /simulation-data/generate",
            "request": {
                "simulation_id": "550e8400-e29b-41d4-a716-446655440000",
                "use_current_simulation": True,
                "start_time": now.isoformat(),
                "end_time": tomorrow.isoformat(),
                "sample_interval_seconds": 1800,  # Every 30 minutes
                "device_ids": [
                    "550e8400-e29b-41d4-a716-446655440001",  # Example device ID 1
                    "550e8400-e29b-41d4-a716-446655440002"   # Example device ID 2
                ]
            },
            "use_case": "Focus on specific high-consumption devices"
        }
    }

def example_response_structure():
    """Show the structure of API responses."""
    
    return {
        "response_structure": {
            "request_config": "Original request configuration",
            "total_data_points": "Number of data points generated",
            "duration_seconds": "Total time period covered",
            "min_consumption": "Minimum consumption value",
            "max_consumption": "Maximum consumption value", 
            "avg_consumption": "Average consumption",
            "total_energy": "Total energy consumed",
            "consumption_unit": "Unit of consumption values",
            "energy_unit": "Unit of energy calculation",
            "data_points": [
                {
                    "timestamp": "ISO datetime",
                    "unix_timestamp": "Unix timestamp",
                    "total_consumption": "Total consumption at this time",
                    "base_consumption": "Electric meter base consumption",
                    "device_consumption": "Sum of all device consumption",
                    "devices": [
                        {
                            "device_id": "UUID",
                            "device_name": "Device name",
                            "consumption": "Device consumption value",
                            "algorithm_type": "Algorithm used"
                        }
                    ]
                }
            ]
        }
    }

def frontend_integration_examples():
    """Examples for frontend integration."""
    
    return {
        "javascript_fetch_example": """
// Example: Get daily consumption preview
async function getDailyPreview() {
    const response = await fetch('/simulation-data/preview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            duration_hours: 24.0,
            time_speed: 60.0,  // 60x speed = see day in 24 minutes
            output_unit: 'W',
            sample_interval_minutes: 5
        })
    });
    
    const data = await response.json();
    
    // Use data for charts
    const chartData = data.data_points.map(point => ({
        time: point.timestamp,
        consumption: point.total_consumption,
        devices: point.devices
    }));
    
    return chartData;
}
        """,
        
        "react_component_example": """
// Example React component for simulation data
import React, { useState } from 'react';

function SimulationDataGenerator() {
    const [config, setConfig] = useState({
        duration_hours: 24,
        time_speed: 1.0,
        output_unit: 'W',
        sample_interval_minutes: 10
    });
    
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    
    const generateData = async () => {
        setLoading(true);
        try {
            const response = await fetch('/simulation-data/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            });
            
            const result = await response.json();
            setData(result);
        } catch (error) {
            console.error('Error generating data:', error);
        } finally {
            setLoading(false);
        }
    };
    
    return (
        <div>
            <h3>Simulation Data Generator</h3>
            
            <div>
                <label>Duration (hours):</label>
                <input 
                    type="number" 
                    value={config.duration_hours}
                    onChange={(e) => setConfig({...config, duration_hours: parseFloat(e.target.value)})}
                />
            </div>
            
            <div>
                <label>Speed:</label>
                <select 
                    value={config.time_speed}
                    onChange={(e) => setConfig({...config, time_speed: parseFloat(e.target.value)})}
                >
                    <option value={1}>Real-time (1x)</option>
                    <option value={60}>Fast (60x - hour in 1 minute)</option>
                    <option value={1440}>Very Fast (1440x - day in 1 minute)</option>
                </select>
            </div>
            
            <div>
                <label>Output Unit:</label>
                <select 
                    value={config.output_unit}
                    onChange={(e) => setConfig({...config, output_unit: e.target.value})}
                >
                    <option value="W">Watts</option>
                    <option value="kW">Kilowatts</option>
                    <option value="kWh/day">kWh per day</option>
                    <option value="kWh/year">kWh per year</option>
                </select>
            </div>
            
            <button onClick={generateData} disabled={loading}>
                {loading ? 'Generating...' : 'Generate Data'}
            </button>
            
            {data && (
                <div>
                    <h4>Results:</h4>
                    <p>Total data points: {data.total_data_points}</p>
                    <p>Average consumption: {data.avg_consumption.toFixed(2)} {data.consumption_unit}</p>
                    <p>Total energy: {data.total_energy.toFixed(2)} {data.energy_unit}</p>
                    
                    {/* Add chart component here */}
                </div>
            )}
        </div>
    );
}

export default SimulationDataGenerator;
        """,
        
        "chart_integration": """
// Example: Integrate with Chart.js
import Chart from 'chart.js/auto';

function createConsumptionChart(data, canvasId) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    const chartData = {
        labels: data.data_points.map(point => 
            new Date(point.timestamp).toLocaleTimeString()
        ),
        datasets: [{
            label: `Total Consumption (${data.consumption_unit})`,
            data: data.data_points.map(point => point.total_consumption),
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1
        }]
    };
    
    // Add device-specific datasets
    if (data.data_points[0]?.devices) {
        const deviceNames = [...new Set(
            data.data_points.flatMap(point => 
                point.devices.map(d => d.device_name)
            )
        )];
        
        deviceNames.forEach((deviceName, index) => {
            const colors = ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)'];
            chartData.datasets.push({
                label: deviceName,
                data: data.data_points.map(point => {
                    const device = point.devices.find(d => d.device_name === deviceName);
                    return device ? device.consumption : 0;
                }),
                borderColor: colors[index % colors.length],
                backgroundColor: colors[index % colors.length] + '20',
                tension: 0.1
            });
        });
    }
    
    new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Consumption Over Time'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: `Consumption (${data.consumption_unit})`
                    }
                }
            }
        }
    });
}
        """
    }

def curl_examples():
    """Curl examples for testing the API."""
    
    return {
        "daily_preview": """
curl -X POST "http://localhost:8000/simulation-data/preview" \\
     -H "Content-Type: application/json" \\
     -d '{
         "duration_hours": 24.0,
         "time_speed": 1.0,
         "output_unit": "W",
         "sample_interval_minutes": 15
     }'
        """,
        
        "fast_analysis": """
curl -X POST "http://localhost:8000/simulation-data/generate" \\
     -H "Content-Type: application/json" \\
     -d '{
         "time_unit": "minutes",
         "time_speed": 60.0,
         "output_unit": "kWh/day",
         "start_time": "2024-01-01T00:00:00",
         "end_time": "2024-01-02T00:00:00",
         "sample_interval_seconds": 300
     }'
        """,
        
        "get_examples": """
curl -X GET "http://localhost:8000/simulation-data/config-examples"
        """,
        
        "get_units": """
curl -X GET "http://localhost:8000/simulation-data/supported-units"
        """
    }

if __name__ == "__main__":
    # Print examples
    examples = example_requests()
    for name, example in examples.items():
        print(f"\n=== {name.upper()} ===")
        print(f"Description: {example['description']}")
        print(f"Endpoint: {example['endpoint']}")
        print(f"Request: {json.dumps(example['request'], indent=2)}")
        print(f"Use case: {example['use_case']}")
    
    print("\n" + "="*50)
    print("Frontend Integration Examples:")
    integration = frontend_integration_examples()
    for key, code in integration.items():
        print(f"\n{key}:\n{code}")