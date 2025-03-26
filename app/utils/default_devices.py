from models.settings_models import Device

refrigerator: Device = Device(
    name="Refrigerator",
    description="A refrigerator is a cooling apparatus. The common household appliance consists of a thermally insulated compartment and a heat pump that transfers heat from its inside to its external environment so that its inside is cooled to a temperature below the room temperature.",
    consumption_value=0.5,
    consumption_algorithm="linear",
    is_default=True
)
