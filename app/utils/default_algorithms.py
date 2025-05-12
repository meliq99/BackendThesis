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

active_ligthtbulb_script = """
def simulate(current_time, base_consumption, _, __, ___, extra_params):
    schedule = extra_params.get('schedule', [(0, 3600)])
    day_time = current_time % 86400
    for start, end in schedule:
        if start <= day_time < end:
            return base_consumption
    # modo standby muy bajo
    return 10
"""
active: ConsumptionAlgorithm = ConsumptionAlgorithm(
    name="Default Active Algorithm",
    description="Consume energía mientras está encendida",
    algorithm_type="active",
    script=active_ligthtbulb_script,
)

tv_script = """
def simulate(current_time, base_consumption, peak_consumption, __, ___, extra_params):
    # extra_params debe incluir 'peak_start' y 'peak_end' en segundos desde medianoche
    peak_start = extra_params.get('peak_start', 18*3600)
    peak_end   = extra_params.get('peak_end', 23*3600)
    # Consumo en modo espera (standby)
    standby = extra_params.get('standby_consumption', base_consumption * 0.1)
    
    # Hora actual del día (segundos desde medianoche)
    day_time = current_time % 86400
    
    # Si está en hora pico
    if peak_start <= day_time < peak_end:
        return peak_consumption
    # Si está en standby temprano o tarde
    elif peak_end <= day_time or day_time < peak_start:
        return standby
    else:
        return 0
"""
schedule: ConsumptionAlgorithm = ConsumptionAlgorithm(
    name="Default Schedule Algorithm.",
    description="Modelo basado en horas pico de uso y consumo en standby fuera de pico.",
    algorithm_type="schedule",
    script=tv_script,
)

fan_script = """
def simulate(current_time, base_consumption, peak_consumption, _, __, extra_params):
    # extra_params incluye 'speed' entero de 1 a 3
    speed = extra_params.get('speed', 1)
    # factor cuadrático típico en aerodinámica
    factor = (speed / 3) ** 2
    return base_consumption + (peak_consumption - base_consumption) * factor
"""
vcyclic: ConsumptionAlgorithm = ConsumptionAlgorithm(
    name="Ventilador Velocidad",
    description="Modelo de consumo según velocidad con relación cuadrática.",
    algorithm_type="speed-based",
    script=fan_script,
)

coffee_script = """
def simulate(current_time, base_consumption, peak_consumption, _, __, extra_params):
    # extra_params: 'brew_start' y 'brew_duration' en segundos, 'keep_duration' en segundos
    brew_start    = extra_params.get('brew_start', 8*3600)  # por defecto 8:00 am
    brew_duration = extra_params.get('brew_duration', 300) # 5 min
    keep_duration = extra_params.get('keep_duration', 3600) # 1 hora
    t = current_time % 86400
    # si está en ciclo de preparación
    if brew_start <= t < brew_start + brew_duration:
        return peak_consumption
    # si está en modo mantener caliente
    elif brew_start + brew_duration <= t < brew_start + brew_duration + keep_duration:
        return base_consumption * 0.5
    else:
        return 0
"""
cactive: ConsumptionAlgorithm = ConsumptionAlgorithm(
    name="Cafetera Brewing/Mantener",
    description="Modelo con ciclo de brew pico y fase de mantener caliente de consumo medio.",
    algorithm_type="cycle",
    script=coffee_script,
)

phone_script = """
def simulate(current_time, base_consumption, peak_consumption, _, _, extra_params):
    # extra_params incluye 'active_interval': duración de actividad en segundos cada hora
    active_interval = extra_params.get('active_interval', 600)  # 10 min/hora
    # Posición en la hora actual
    pos = current_time % 3600
    # Si está en periodo activo
    if pos < active_interval:
        return peak_consumption
    else:
        return base_consumption * 0.2  # standby = 20% consumo base
"""
sactive: ConsumptionAlgorithm = ConsumptionAlgorithm(
    name="Smartphone Ciclo Activo/Standby",
    description="Modelo de uso con fases de actividad y standby cada hora.",
    algorithm_type="cyclic",
    script=phone_script,
)
wifi_script = """
import random

def simulate(current_time, base_consumption, _, _, _, extra_params):
    # base_consumption es el consumo típico en W (ej. 4.64W)
    # Variación aleatoria de ±5%
    variation = random.uniform(-0.05, 0.05)
    return base_consumption * (1 + variation)
"""
wactive: ConsumptionAlgorithm = ConsumptionAlgorithm(
    name="Router WiFi Constante",
    description="Modelo con consumo base constante y pequeña variación aleatoria por carga.",
    algorithm_type="constant",
    script=wifi_script,
)