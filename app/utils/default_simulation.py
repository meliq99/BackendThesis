from models.simulation_models import Simulation
from datetime import datetime


default_simulation = Simulation(
    name="First Simulation",
    is_active=True,
    output_unit="W",           # Default to watts
    time_unit="seconds",       # Default to seconds
    time_speed=1.0,           # Default to real-time
    simulation_start_time=None # Default to current time
)
