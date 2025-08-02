"""
Service for generating simulation data over specified time periods.
This allows users to analyze consumption patterns and preview simulation results.
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session

from schemes.simulation_data_schemes import (
    SimulationDataRequest, 
    SimulationDataResponse, 
    SimulationDataPoint,
    DeviceConsumptionPoint,
    SimulationPreviewRequest
)
from models.simulation_models import Simulation
from repository import electric_meter_repository, device_simulation_repository, simulation_repository
from services import simulation_service
from utils.publisher import execute_custom_simulation, get_consumption_algorithms
from utils.unit_converter import watts_to_unit, get_time_multiplier

async def generate_simulation_data(request: SimulationDataRequest, session: Session) -> SimulationDataResponse:
    """
    Generate simulation data for the specified time period and configuration.
    
    Args:
        request: Configuration for data generation
        session: Database session
        
    Returns:
        Generated simulation data with statistics
    """
    
    # Get simulation
    simulation = session.get(Simulation, request.simulation_id)
    if not simulation:
        raise ValueError(f"Simulation not found: {request.simulation_id}")
    
    # Determine configuration to use
    if request.use_current_simulation:
        # Use simulation's configuration
        time_unit = simulation.time_unit
        time_speed = simulation.time_speed
        output_unit = simulation.output_unit
    else:
        # Use overrides (with defaults if not provided)
        time_unit = request.time_unit or "seconds"
        time_speed = request.time_speed or 1.0
        output_unit = request.output_unit or "W"
    
    # Get electric meter
    electric_meter = electric_meter_repository.get_electric_meter(simulation.id, session)
    
    # Get devices to simulate
    if request.device_ids:
        # Use specific devices
        device_simulations = []
        for device_id in request.device_ids:
            device_sims = device_simulation_repository.get_device_simulations(electric_meter.id, session)
            device_simulations.extend([d for d in device_sims if d.id in request.device_ids])
    else:
        # Use all devices in current simulation
        device_simulations = device_simulation_repository.get_device_simulations(electric_meter.id, session)
    
    # Calculate time parameters
    start_timestamp = int(request.start_time.timestamp())
    end_timestamp = int(request.end_time.timestamp())
    duration_seconds = end_timestamp - start_timestamp
    time_multiplier = get_time_multiplier(time_unit)
    
    # Generate data points
    data_points = []
    current_timestamp = start_timestamp
    
    consumption_values = []  # For statistics
    
    while current_timestamp <= end_timestamp:
        # Calculate consumption at this time point
        device_consumptions = []
        total_device_consumption = 0
        
        # Calculate simulation time based on speed
        simulation_time = calculate_simulation_time_for_timestamp(
            current_timestamp, 
            time_speed,
            start_timestamp
        )
        
        for device_simulation in device_simulations:
            # Get algorithm script
            algorithm_script = await get_consumption_algorithms(device_simulation.algorithm_id, session)
            
            # Get algorithm info
            algorithm = simulation_repository.get_consumption_algorithm_by_id(device_simulation.algorithm_id, session)
            
            try:
                # Prepare extra_params
                extra_params = {
                    "base_interval": time_multiplier,
                    "time_unit": time_unit,
                    "time_speed": time_speed,
                    "factor": 1.0
                }
                
                # Calculate device consumption
                device_consumption = execute_custom_simulation(
                    custom_script=algorithm_script,
                    current_time=simulation_time,
                    base_consumption=device_simulation.consumption_value,
                    peak_consumption=device_simulation.peak_consumption,
                    cycle_duration=device_simulation.cycle_duration,
                    on_duration=device_simulation.on_duration,
                    extra_params=extra_params
                )
                
                device_consumptions.append(DeviceConsumptionPoint(
                    device_id=device_simulation.id,
                    device_name=device_simulation.name,
                    consumption=device_consumption,
                    algorithm_type=algorithm.algorithm_type
                ))
                
                total_device_consumption += device_consumption
                
            except Exception as e:
                print(f"Error calculating consumption for device {device_simulation.id}: {e}")
                device_consumptions.append(DeviceConsumptionPoint(
                    device_id=device_simulation.id,
                    device_name=device_simulation.name,
                    consumption=0.0,
                    algorithm_type=algorithm.algorithm_type if algorithm else "unknown"
                ))
        
        # Total consumption (devices + base)
        total_consumption_watts = total_device_consumption + electric_meter.base_consumption
        
        # Convert to output unit
        total_consumption_output = watts_to_unit(total_consumption_watts, output_unit)
        base_consumption_output = watts_to_unit(electric_meter.base_consumption, output_unit)
        device_consumption_output = watts_to_unit(total_device_consumption, output_unit)
        
        # Convert device consumptions to output unit
        for device_point in device_consumptions:
            device_point.consumption = watts_to_unit(device_point.consumption, output_unit)
        
        # Create data point
        data_point = SimulationDataPoint(
            timestamp=datetime.fromtimestamp(current_timestamp),
            unix_timestamp=current_timestamp,
            total_consumption=total_consumption_output,
            base_consumption=base_consumption_output,
            device_consumption=device_consumption_output,
            devices=device_consumptions
        )
        
        data_points.append(data_point)
        consumption_values.append(total_consumption_output)
        
        # Move to next sample
        current_timestamp += request.sample_interval_seconds
    
    # Calculate statistics
    min_consumption = min(consumption_values) if consumption_values else 0
    max_consumption = max(consumption_values) if consumption_values else 0
    avg_consumption = sum(consumption_values) / len(consumption_values) if consumption_values else 0
    
    # Calculate total energy (approximate using average consumption)
    duration_hours = duration_seconds / 3600
    total_energy = calculate_total_energy(avg_consumption, duration_hours, output_unit)
    energy_unit = get_energy_unit(output_unit)
    
    return SimulationDataResponse(
        request_config=request,
        total_data_points=len(data_points),
        duration_seconds=duration_seconds,
        min_consumption=min_consumption,
        max_consumption=max_consumption,
        avg_consumption=avg_consumption,
        total_energy=total_energy,
        consumption_unit=output_unit,
        energy_unit=energy_unit,
        data_points=data_points
    )

async def generate_simulation_preview(request: SimulationPreviewRequest, session: Session) -> SimulationDataResponse:
    """
    Generate a quick preview of simulation data.
    
    Args:
        request: Preview configuration
        session: Database session
        
    Returns:
        Generated simulation data
    """
    # Convert preview request to full request
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=request.duration_hours)
    sample_interval = request.sample_interval_minutes * 60  # Convert to seconds
    
    full_request = SimulationDataRequest(
        simulation_id=request.simulation_id,
        use_current_simulation=request.use_current_simulation,
        start_time=start_time,
        end_time=end_time,
        sample_interval_seconds=sample_interval,
        device_ids=None,  # Use all devices
        # Overrides (only used if use_current_simulation=False)
        time_unit=None,  # Will default to "seconds" if overriding
        time_speed=request.time_speed,
        output_unit=request.output_unit
    )
    
    return await generate_simulation_data(full_request, session)

def calculate_simulation_time_for_timestamp(current_timestamp: int, time_speed: float, start_timestamp: int) -> int:
    """
    Calculate simulation time for a given timestamp with speed multiplier.
    
    Args:
        current_timestamp: Current timestamp being processed
        time_speed: Speed multiplier
        start_timestamp: Starting timestamp
        
    Returns:
        Simulation time to use for algorithms
    """
    # Calculate elapsed time from start
    elapsed_real = current_timestamp - start_timestamp
    
    # Apply speed multiplier
    elapsed_simulation = elapsed_real * time_speed
    
    # Return simulation time
    return int(start_timestamp + elapsed_simulation)

def calculate_total_energy(avg_consumption: float, duration_hours: float, output_unit: str) -> float:
    """
    Calculate total energy consumption based on average consumption and duration.
    
    Args:
        avg_consumption: Average consumption in output_unit
        duration_hours: Duration in hours
        output_unit: Unit of consumption
        
    Returns:
        Total energy consumed
    """
    if output_unit == "W":
        # Watts to kWh: (W * hours) / 1000
        return (avg_consumption * duration_hours) / 1000
    elif output_unit == "kW":
        # kW to kWh: kW * hours
        return avg_consumption * duration_hours
    elif "kWh" in output_unit:
        # Already energy unit - multiply by duration factor
        if "year" in output_unit:
            return avg_consumption * (duration_hours / 8760)  # Hours in year
        elif "month" in output_unit:
            return avg_consumption * (duration_hours / 720)   # Hours in month
        elif "day" in output_unit:
            return avg_consumption * (duration_hours / 24)    # Hours in day
    
    return avg_consumption * duration_hours

def get_energy_unit(output_unit: str) -> str:
    """Get appropriate energy unit based on output unit."""
    if output_unit in ["W", "kW"]:
        return "kWh"
    elif "kWh" in output_unit:
        return output_unit
    else:
        return "kWh"