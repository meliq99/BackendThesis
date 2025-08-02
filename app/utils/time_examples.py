"""
Examples and test cases for the new time configuration system.
This file demonstrates various time configurations and their effects.
"""

from datetime import datetime, timedelta
from utils.unit_converter import (
    convert_time_to_seconds, 
    convert_seconds_to_time_unit, 
    get_time_multiplier,
    TimeUnit
)

def example_time_configurations():
    """Examples of different time configurations and their use cases."""
    
    print("=== Time Configuration Examples ===\n")
    
    # Example 1: Real-time simulation (default)
    print("1. Real-time Simulation (Default):")
    print("   time_unit: 'seconds'")
    print("   time_speed: 1.0")
    print("   simulation_start_time: None")
    print("   → Algorithms run with actual wall-clock time")
    print("   → Perfect for real-time monitoring\n")
    
    # Example 2: Accelerated simulation
    print("2. Accelerated Simulation (1 hour = 1 minute):")
    print("   time_unit: 'minutes'")
    print("   time_speed: 60.0")
    print("   simulation_start_time: None")
    print("   → 1 real minute = 1 simulated hour")
    print("   → See daily patterns in 24 minutes")
    print("   → Great for testing daily cycles\n")
    
    # Example 3: Historical replay
    print("3. Historical Replay:")
    print("   time_unit: 'hours'")
    print("   time_speed: 24.0")
    print("   simulation_start_time: '2024-01-01 00:00:00'")
    print("   → Start from New Year's Day")
    print("   → 1 real hour = 1 simulated day")
    print("   → Replay entire year in ~15 days\n")
    
    # Example 4: Ultra-fast testing
    print("4. Ultra-fast Testing:")
    print("   time_unit: 'hours'")
    print("   time_speed: 8760.0  # Hours in a year")
    print("   simulation_start_time: '2024-01-01 00:00:00'")
    print("   → 1 real hour = 1 simulated year")
    print("   → Test yearly patterns quickly\n")
    
    # Example 5: Slow-motion analysis
    print("5. Slow-motion Analysis:")
    print("   time_unit: 'seconds'")
    print("   time_speed: 0.1")
    print("   simulation_start_time: None")
    print("   → 10 real seconds = 1 simulated second")
    print("   → Detailed analysis of fast patterns\n")

def algorithm_behavior_examples():
    """Show how different algorithms behave with time configurations."""
    
    print("=== Algorithm Behavior Examples ===\n")
    
    # Cyclic algorithm behavior
    print("Cyclic Algorithm (Refrigerator):")
    print("base_interval = get_time_multiplier(time_unit)")
    print("actual_cycle_duration = cycle_duration * base_interval")
    print("")
    print("With time_unit='seconds': base_interval=1")
    print("  cycle_duration=10 → actual_cycle=10 seconds")
    print("With time_unit='minutes': base_interval=60")
    print("  cycle_duration=10 → actual_cycle=600 seconds (10 minutes)")
    print("With time_unit='hours': base_interval=3600")
    print("  cycle_duration=10 → actual_cycle=36000 seconds (10 hours)\n")
    
    # Daily schedule algorithm
    print("Daily Schedule Algorithm (TV):")
    print("day_time = current_time % 86400  # Always 24-hour cycle")
    print("peak_start = 18*3600  # 6 PM")
    print("peak_end = 23*3600    # 11 PM")
    print("")
    print("With time_speed=1.0: Real-time daily pattern")
    print("With time_speed=24.0: Daily pattern in 1 hour")
    print("With time_speed=1440.0: Daily pattern in 1 minute\n")

def test_time_conversions():
    """Test the time conversion functions."""
    
    print("=== Time Conversion Tests ===\n")
    
    # Test basic conversions
    test_cases = [
        (1, "minutes", "seconds"),  # 1 minute = 60 seconds
        (1, "hours", "minutes"),    # 1 hour = 60 minutes
        (1, "days", "hours"),       # 1 day = 24 hours
        (1, "hours", "seconds"),    # 1 hour = 3600 seconds
    ]
    
    for value, from_unit, to_unit in test_cases:
        seconds = convert_time_to_seconds(value, from_unit)
        converted = convert_seconds_to_time_unit(seconds, to_unit)
        print(f"{value} {from_unit} = {converted} {to_unit}")
    
    print()
    
    # Test multipliers
    print("Time Multipliers:")
    for unit in ["seconds", "minutes", "hours", "days"]:
        multiplier = get_time_multiplier(unit)
        print(f"{unit}: {multiplier}")

def real_world_scenarios():
    """Real-world testing scenarios."""
    
    print("\n=== Real-World Testing Scenarios ===\n")
    
    scenarios = [
        {
            "name": "Development Testing",
            "config": {
                "time_unit": "minutes",
                "time_speed": 60.0,
                "simulation_start_time": None
            },
            "description": "Test daily patterns in 24 minutes"
        },
        {
            "name": "Energy Audit Simulation",
            "config": {
                "time_unit": "hours",
                "time_speed": 168.0,  # Week in 1 hour
                "simulation_start_time": "2024-01-01 00:00:00"
            },
            "description": "Simulate weekly consumption patterns"
        },
        {
            "name": "Real-time Monitoring",
            "config": {
                "time_unit": "seconds",
                "time_speed": 1.0,
                "simulation_start_time": None
            },
            "description": "Live consumption monitoring"
        },
        {
            "name": "Historical Analysis",
            "config": {
                "time_unit": "days",
                "time_speed": 30.0,  # Month in 1 day
                "simulation_start_time": "2023-01-01 00:00:00"
            },
            "description": "Analyze year-long patterns"
        }
    ]
    
    for scenario in scenarios:
        print(f"Scenario: {scenario['name']}")
        print(f"Description: {scenario['description']}")
        config = scenario['config']
        for key, value in config.items():
            print(f"  {key}: {value}")
        print()

if __name__ == "__main__":
    example_time_configurations()
    algorithm_behavior_examples()
    test_time_conversions()
    real_world_scenarios()