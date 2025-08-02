"""
Schemas for simulation data generation endpoint.
This allows users to generate consumption data for analysis and preview.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID

class SimulationDataRequest(BaseModel):
    """Request schema for generating simulation data."""
    
    # Simulation configuration
    simulation_id: UUID = Field(description="Simulation ID to use for device and configuration data")
    use_current_simulation: bool = Field(default=True, description="Use simulation's time/unit config. If false, override with provided values")
    
    # Time range for data generation (mandatory)
    start_time: datetime = Field(description="Start time for simulation data generation")
    end_time: datetime = Field(description="End time for simulation data generation")
    sample_interval_seconds: int = Field(default=60, description="Interval between data points in seconds")
    
    # Configuration overrides (only used when use_current_simulation=False)
    time_unit: Optional[str] = Field(default=None, description="Override time unit (seconds, minutes, hours, days)")
    time_speed: Optional[float] = Field(default=None, description="Override simulation speed multiplier")
    output_unit: Optional[str] = Field(default=None, description="Override output unit (W, kW, kWh/year, kWh/month)")
    
    # Device selection (optional - if not provided, uses all simulation devices)
    device_ids: Optional[List[UUID]] = Field(default=None, description="Specific device IDs to include (optional)")

class SimulationDataPoint(BaseModel):
    """Single data point in simulation results."""
    
    timestamp: datetime = Field(description="Timestamp for this data point")
    unix_timestamp: int = Field(description="Unix timestamp in seconds")
    total_consumption: float = Field(description="Total consumption at this time point")
    base_consumption: float = Field(description="Base electric meter consumption")
    device_consumption: float = Field(description="Total device consumption")
    devices: List["DeviceConsumptionPoint"] = Field(description="Individual device consumption breakdown")

class DeviceConsumptionPoint(BaseModel):
    """Consumption data for a single device at a specific time."""
    
    device_id: UUID = Field(description="Device ID")
    device_name: str = Field(description="Device name")
    consumption: float = Field(description="Device consumption at this time point")
    algorithm_type: str = Field(description="Algorithm type used")

class SimulationDataResponse(BaseModel):
    """Response schema for generated simulation data."""
    
    # Request metadata
    request_config: SimulationDataRequest = Field(description="Original request configuration")
    
    # Summary statistics
    total_data_points: int = Field(description="Total number of data points generated")
    duration_seconds: int = Field(description="Total duration covered in seconds")
    
    # Consumption statistics
    min_consumption: float = Field(description="Minimum consumption value")
    max_consumption: float = Field(description="Maximum consumption value")
    avg_consumption: float = Field(description="Average consumption value")
    total_energy: float = Field(description="Total energy consumed over the period")
    
    # Units and metadata
    consumption_unit: str = Field(description="Unit of consumption values")
    energy_unit: str = Field(description="Unit of total energy calculation")
    
    # Generated data
    data_points: List[SimulationDataPoint] = Field(description="Generated simulation data points")

class SimulationPreviewRequest(BaseModel):
    """Simplified request for quick simulation preview."""
    
    simulation_id: UUID = Field(description="Simulation ID to use")
    duration_hours: float = Field(default=24.0, description="Duration to simulate in hours")
    use_current_simulation: bool = Field(default=True, description="Use simulation's configuration")
    sample_interval_minutes: int = Field(default=5, description="Sampling interval in minutes")
    
    # Configuration overrides (only used when use_current_simulation=False)
    time_speed: Optional[float] = Field(default=None, description="Override simulation speed multiplier")
    output_unit: Optional[str] = Field(default=None, description="Override output unit for results")

# Update forward references
SimulationDataPoint.model_rebuild()