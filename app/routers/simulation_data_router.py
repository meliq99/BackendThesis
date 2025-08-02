"""
Router for simulation data generation endpoints.
Provides endpoints to generate and analyze consumption data over time periods.
"""

from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from utils.get_db_connection import get_session
from schemes.simulation_data_schemes import (
    SimulationDataRequest, 
    SimulationDataResponse,
    SimulationPreviewRequest
)
from services.simulation_data_service import generate_simulation_data, generate_simulation_preview

router = APIRouter(prefix="/simulation-data", tags=["Simulation Data"])

SessionDependency = Annotated[Session, Depends(get_session)]

@router.post("/generate", response_model=SimulationDataResponse)
async def generate_data(
    request: SimulationDataRequest, 
    session: SessionDependency
) -> Any:
    """
    Generate simulation data for a specified time period and configuration.
    
    This endpoint uses a simulation ID to get device and configuration data:
    - **simulation_id**: Required - specifies which simulation to analyze
    - **use_current_simulation**: If true, uses simulation's time/unit config
    - **Time range**: start_time and end_time are always required
    - **Overrides**: When use_current_simulation=false, provide custom config
    
    Example using simulation config:
    ```json
    {
        "simulation_id": "550e8400-e29b-41d4-a716-446655440000",
        "use_current_simulation": true,
        "start_time": "2024-01-01T00:00:00",
        "end_time": "2024-01-02T00:00:00",
        "sample_interval_seconds": 3600
    }
    ```
    
    Example with custom overrides:
    ```json
    {
        "simulation_id": "550e8400-e29b-41d4-a716-446655440000", 
        "use_current_simulation": false,
        "start_time": "2024-01-01T00:00:00",
        "end_time": "2024-01-02T00:00:00",
        "sample_interval_seconds": 3600,
        "time_unit": "hours",
        "time_speed": 24.0,
        "output_unit": "kWh/day"
    }
    ```
    
    Returns detailed consumption data with:
    - Individual data points over time
    - Device-level breakdown  
    - Statistical summary (min, max, avg, total energy)
    - Configuration metadata
    """
    try:
        return await generate_simulation_data(request, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating simulation data: {str(e)}")

@router.post("/preview", response_model=SimulationDataResponse)
async def generate_preview(
    request: SimulationPreviewRequest,
    session: SessionDependency
) -> Any:
    """
    Generate a quick preview of simulation data.
    
    Simplified endpoint for quick analysis starting from current time.
    Perfect for frontend previews and quick consumption estimates.
    
    Example using simulation config:
    ```json
    {
        "simulation_id": "550e8400-e29b-41d4-a716-446655440000",
        "duration_hours": 24.0,
        "use_current_simulation": true,
        "sample_interval_minutes": 10
    }
    ```
    
    Example with custom overrides:
    ```json
    {
        "simulation_id": "550e8400-e29b-41d4-a716-446655440000",
        "duration_hours": 24.0,
        "use_current_simulation": false,
        "time_speed": 60.0,
        "output_unit": "W",
        "sample_interval_minutes": 10
    }
    ```
    
    Returns:
    - Consumption data for specified duration
    - Uses specified simulation and all its devices
    - Starts from current time
    - Optionally override simulation configuration
    """
    try:
        return await generate_simulation_preview(request, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating preview: {str(e)}")

@router.get("/config-examples")
async def get_configuration_examples() -> Any:
    """
    Get example configurations for different use cases.
    
    Returns common configuration patterns for:
    - Real-time analysis
    - Daily pattern preview
    - Weekly analysis
    - Monthly overview
    - Historical replay
    """
    return {
        "real_time_analysis": {
            "description": "Analyze current consumption in real-time",
            "config": {
                "time_unit": "seconds",
                "time_speed": 1.0,
                "output_unit": "W",
                "duration_hours": 1.0,
                "sample_interval_minutes": 1
            }
        },
        "daily_pattern_preview": {
            "description": "See daily patterns in 24 minutes",
            "config": {
                "time_unit": "minutes", 
                "time_speed": 60.0,
                "output_unit": "W",
                "duration_hours": 24.0,
                "sample_interval_minutes": 1
            }
        },
        "weekly_analysis": {
            "description": "Analyze weekly patterns quickly",
            "config": {
                "time_unit": "hours",
                "time_speed": 168.0,
                "output_unit": "kWh/day",
                "duration_hours": 168.0,
                "sample_interval_minutes": 60
            }
        },
        "monthly_overview": {
            "description": "Monthly consumption overview",
            "config": {
                "time_unit": "days",
                "time_speed": 30.0,
                "output_unit": "kWh/month",
                "duration_hours": 720.0,
                "sample_interval_minutes": 360
            }
        },
        "historical_replay": {
            "description": "Replay specific historical period",
            "config": {
                "time_unit": "hours",
                "time_speed": 24.0,
                "output_unit": "kWh/year",
                "start_time": "2024-01-01T00:00:00",
                "end_time": "2024-12-31T23:59:59",
                "sample_interval_seconds": 86400
            }
        }
    }

@router.get("/supported-units")
async def get_supported_units() -> Any:
    """
    Get all supported units for time and consumption.
    
    Returns:
    - Available time units
    - Available output units  
    - Valid time speed ranges
    - Sampling interval recommendations
    """
    return {
        "time_units": {
            "seconds": "Real-time granularity, base unit",
            "minutes": "Minute-based algorithms and sampling",
            "hours": "Hourly patterns and analysis", 
            "days": "Daily cycles and long-term patterns"
        },
        "output_units": {
            "W": "Watts - instantaneous power",
            "kW": "Kilowatts - larger power values",
            "kWh/day": "Kilowatt-hours per day",
            "kWh/month": "Kilowatt-hours per month",
            "kWh/year": "Kilowatt-hours per year"
        },
        "time_speed_ranges": {
            "slow_motion": "0.1 - 0.9 (slower than real-time)",
            "real_time": "1.0 (normal speed)",
            "accelerated": "1.1 - 100.0 (faster than real-time)",
            "ultra_fast": "100+ (very fast analysis)"
        },
        "sample_interval_recommendations": {
            "real_time": "1-60 seconds",
            "hourly_analysis": "300-3600 seconds (5-60 minutes)", 
            "daily_analysis": "3600-21600 seconds (1-6 hours)",
            "weekly_analysis": "21600-86400 seconds (6-24 hours)"
        }
    }