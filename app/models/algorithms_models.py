from sqlmodel import Field, SQLModel
import uuid

# We'll use the existing ConsumptionAlgorithm table from simulation_models.py
# This file serves as a reference/alias for consistency with the project structure
from models.simulation_models import ConsumptionAlgorithm

# Export the model so it can be imported from this module
__all__ = ["ConsumptionAlgorithm"]
