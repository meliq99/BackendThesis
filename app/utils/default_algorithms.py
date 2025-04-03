from models.simulation_models import ConsumptionAlgorithm

cyclic_script = """
def simulate(current_time, base_consumption, peak_consumption, cycle_duration, on_duration, extra_params):
    # extra_params debe incluir "base_interval": el intervalo de simulación en segundos (por ejemplo, 2)
    base_interval = extra_params.get("base_interval", 2)
    factor = extra_params.get("factor", 1)
    
    # Calcula la duración real del ciclo y del período activo en segundos.
    # Por ejemplo, si cycle_duration es 10 y base_interval es 2, el ciclo dura 10*2 = 20 segundos.
    # Si on_duration es 1, el período activo dura 1*2 = 2 segundos.
    actual_cycle_duration = cycle_duration * base_interval
    actual_on_duration = on_duration * base_interval
    
    # Calcula la posición actual dentro del ciclo.
    cycle_position = current_time % actual_cycle_duration
    
    # Durante el período "on" se aplica el consumo pico, el resto se usa el consumo base.
    if cycle_position < actual_on_duration:
        return peak_consumption * factor
    else:
        return base_consumption * factor
"""

cyclic: ConsumptionAlgorithm = ConsumptionAlgorithm(
    name="Default Cyclic Algorithm",
    description="This algorithm is a simple cyclic algorithm that consumes resources in a cyclic manner.",
    algorithm_type="cyclic",
    script=cyclic_script,
)