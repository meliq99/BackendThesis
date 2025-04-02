from models.simulation_models import ConsumptionAlgorithm

cyclic_script = """
def simulate(current_time, base_consumption, peak_consumption, cycle_duration, on_duration, extra_params):
    return base_consumption + peak_consumption
"""

cyclic: ConsumptionAlgorithm = ConsumptionAlgorithm(
    name="Default Cyclic Algorithm",
    description="This algorithm is a simple cyclic algorithm that consumes resources in a cyclic manner.",
    algorithm_type="cyclic",
    script=cyclic_script,
)