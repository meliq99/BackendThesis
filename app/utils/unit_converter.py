"""
Unit conversion utilities for power and energy calculations.
All internal calculations are done in watts (W), and this module handles
conversion to different units for frontend display.
"""

from typing import Literal

# Type definition for supported units
PowerUnit = Literal["W", "kW", "kWh/year", "kWh/month", "kWh/day"]
TimeUnit = Literal["seconds", "minutes", "hours", "days"]

# Constants for conversions
WATTS_PER_KILOWATT = 1000
HOURS_PER_DAY = 24
DAYS_PER_MONTH = 30  # Average for monthly calculations
DAYS_PER_YEAR = 365
HOURS_PER_MONTH = DAYS_PER_MONTH * HOURS_PER_DAY
HOURS_PER_YEAR = DAYS_PER_YEAR * HOURS_PER_DAY

# Time conversion constants
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400


def watts_to_unit(watts: float, target_unit: PowerUnit) -> float:
    """
    Convert watts to the specified unit.
    
    Args:
        watts: Power consumption in watts
        target_unit: Target unit for conversion
        
    Returns:
        Converted value in target unit
        
    Raises:
        ValueError: If target_unit is not supported
    """
    if target_unit == "W":
        return watts
    elif target_unit == "kW":
        return watts / WATTS_PER_KILOWATT
    elif target_unit == "kWh/day":
        # Convert watts to kWh consumed per day
        return (watts * HOURS_PER_DAY) / WATTS_PER_KILOWATT
    elif target_unit == "kWh/month":
        # Convert watts to kWh consumed per month (30 days average)
        return (watts * HOURS_PER_MONTH) / WATTS_PER_KILOWATT
    elif target_unit == "kWh/year":
        # Convert watts to kWh consumed per year
        return (watts * HOURS_PER_YEAR) / WATTS_PER_KILOWATT
    else:
        raise ValueError(f"Unsupported unit: {target_unit}")


def unit_to_watts(value: float, source_unit: PowerUnit) -> float:
    """
    Convert from specified unit to watts.
    
    Args:
        value: Value in source unit
        source_unit: Source unit
        
    Returns:
        Value converted to watts
        
    Raises:
        ValueError: If source_unit is not supported
    """
    if source_unit == "W":
        return value
    elif source_unit == "kW":
        return value * WATTS_PER_KILOWATT
    elif source_unit == "kWh/day":
        # Convert kWh per day to average watts
        return (value * WATTS_PER_KILOWATT) / HOURS_PER_DAY
    elif source_unit == "kWh/month":
        # Convert kWh per month to average watts
        return (value * WATTS_PER_KILOWATT) / HOURS_PER_MONTH
    elif source_unit == "kWh/year":
        # Convert kWh per year to average watts
        return (value * WATTS_PER_KILOWATT) / HOURS_PER_YEAR
    else:
        raise ValueError(f"Unsupported unit: {source_unit}")


def get_unit_display_name(unit: PowerUnit) -> str:
    """
    Get user-friendly display name for unit.
    
    Args:
        unit: Power unit
        
    Returns:
        Human-readable unit name
    """
    unit_names = {
        "W": "Watts",
        "kW": "Kilowatts", 
        "kWh/day": "kWh por día",
        "kWh/month": "kWh por mes",
        "kWh/year": "kWh por año"
    }
    return unit_names.get(unit, unit)


def is_valid_unit(unit: str) -> bool:
    """
    Check if unit is supported.
    
    Args:
        unit: Unit string to validate
        
    Returns:
        True if unit is supported
    """
    return unit in ["W", "kW", "kWh/day", "kWh/month", "kWh/year"]


def convert_time_to_seconds(value: float, source_unit: TimeUnit) -> float:
    """
    Convert time value to seconds.
    
    Args:
        value: Time value in source unit
        source_unit: Source time unit
        
    Returns:
        Time value converted to seconds
        
    Raises:
        ValueError: If source_unit is not supported
    """
    if source_unit == "seconds":
        return value
    elif source_unit == "minutes":
        return value * SECONDS_PER_MINUTE
    elif source_unit == "hours":
        return value * SECONDS_PER_HOUR
    elif source_unit == "days":
        return value * SECONDS_PER_DAY
    else:
        raise ValueError(f"Unsupported time unit: {source_unit}")


def convert_seconds_to_time_unit(seconds: float, target_unit: TimeUnit) -> float:
    """
    Convert seconds to specified time unit.
    
    Args:
        seconds: Time value in seconds
        target_unit: Target time unit
        
    Returns:
        Time value converted to target unit
        
    Raises:
        ValueError: If target_unit is not supported
    """
    if target_unit == "seconds":
        return seconds
    elif target_unit == "minutes":
        return seconds / SECONDS_PER_MINUTE
    elif target_unit == "hours":
        return seconds / SECONDS_PER_HOUR
    elif target_unit == "days":
        return seconds / SECONDS_PER_DAY
    else:
        raise ValueError(f"Unsupported time unit: {target_unit}")


def get_time_multiplier(time_unit: TimeUnit) -> int:
    """
    Get multiplier for time unit conversion to seconds.
    Used for algorithm base_interval parameter.
    
    Args:
        time_unit: Time unit
        
    Returns:
        Multiplier to convert to seconds
    """
    multipliers = {
        "seconds": 1,
        "minutes": SECONDS_PER_MINUTE,
        "hours": SECONDS_PER_HOUR,
        "days": SECONDS_PER_DAY
    }
    return multipliers.get(time_unit, 1)


def is_valid_time_unit(unit: str) -> bool:
    """
    Check if time unit is supported.
    
    Args:
        unit: Time unit string to validate
        
    Returns:
        True if time unit is supported
    """
    return unit in ["seconds", "minutes", "hours", "days"]


# Example usage and test values
if __name__ == "__main__":
    # Test refrigerator example: 42W average -> should be ~368 kWh/year
    test_watts = 42.0
    kwh_year = watts_to_unit(test_watts, "kWh/year")
    print(f"{test_watts}W = {kwh_year:.1f} kWh/year")
    
    # Test reverse conversion
    back_to_watts = unit_to_watts(kwh_year, "kWh/year")
    print(f"{kwh_year:.1f} kWh/year = {back_to_watts:.1f}W")