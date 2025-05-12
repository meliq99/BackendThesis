from models.settings_models import Device

refrigerator: Device = Device(
    name="Refrigerator",
    description="A refrigerator is a cooling apparatus. The common household appliance consists of a thermally insulated compartment and a heat pump that transfers heat from its inside to its external environment so that its inside is cooled to a temperature below the room temperature.",
    consumption_value=50,
    icon="refrigerator",
    is_default=True,
    peak_consumption=200,
    cycle_duration=10,
    on_duration=5
)

lightbulb: Device = Device(
    name="Lightbulb",
    description="A standard light bulb that provides illumination in homes and offices.",
    consumption_value=5.0,
    icon="lightbulb",
    is_default=True,
    peak_consumption=0.08,
    cycle_duration=2,
    on_duration=10,
  )

tv: Device = Device(
    name="Tv",
    description="A television used for multimedia entertainment, with various features and connectivity options.",
    consumption_value=0.15,
    icon="tv",
    is_default=True,
    peak_consumption=0.3,
    cycle_duration=3,
    on_duration=3
)
fan: Device = Device(
    name="Fan",
    description="An electric fan that provides cooling through air circulation.",
    consumption_value=0.08,
    icon="fan",
    is_default=True,
    peak_consumption=0.1,
    cycle_duration=2,
    on_duration=2
)
smartphone: Device = Device(
    name="Smartphone",
    description="A mobile device with multiple functionalities beyond la simple comunicación.",
    consumption_value=0.02,
    icon="smartphone",
    is_default=True,
    peak_consumption=0.05,
    cycle_duration=1,
    on_duration=1
)

coffeemaker: Device = Device(
    name="Coffee Maker",
    description="A machine used to brew coffee, perfect for homes and offices.",
    consumption_value=0.9,
    icon="coffee",
    is_default=True,
    peak_consumption=1.2,
    cycle_duration=5,
    on_duration=4
)

wifi: Device = Device(
    name="Wifi",
    description="A WiFi router that provides wireless connectivity for various devices.",
    consumption_value=0.05,
    icon="wifi",
    is_default=True,
    peak_consumption=0.07,
    cycle_duration=3,
    on_duration=2
)