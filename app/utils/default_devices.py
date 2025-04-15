from models.settings_models import Device

refrigerator: Device = Device(
    name="Refrigerator",
    description="A refrigerator is a cooling apparatus. The common household appliance consists of a thermally insulated compartment and a heat pump that transfers heat from its inside to its external environment so that its inside is cooled to a temperature below the room temperature.",
    consumption_value=50,
    is_default=True,
    peak_consumption=200,
    cycle_duration=10,
    on_duration=5
)

# lightbulb: Device = Device(
#     name="Lightbulb",
#     description="A standard light bulb that provides illumination in homes and offices.",
#     consumption_value=0.06,
#     is_default=True,
#     peak_consumption=0.08,
#     cycle_duration=2,
#     on_duration=10,
#   )
