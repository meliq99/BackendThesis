from models.settings_models import Device

refrigerator: Device = Device(
    name="Refrigerator",
    description="A refrigerator is a cooling apparatus. The common household appliance consists of a thermally insulated compartment and a heat pump that transfers heat from its inside to its external environment so that its inside is cooled to a temperature below the room temperature.",
    consumption_value=25.0,  # 25W standby (lights, electronics)
    icon="refrigerator",
    is_default=True,
    peak_consumption=120.0,  # 120W when compressor runs (averages ~42W total)
    cycle_duration=10,
    on_duration=5
)

lightbulb: Device = Device(
    name="LED Lightbulb",
    description="A standard LED light bulb that provides illumination in homes and offices.",
    consumption_value=9.0,   # 9W LED bulb (equivalent to 60W incandescent)
    icon="lightbulb",
    is_default=True,
    peak_consumption=12.0,   # 12W during startup/dimming
    cycle_duration=2,
    on_duration=10,
  )

tv: Device = Device(
    name="Smart TV",
    description="A television used for multimedia entertainment, with various features and connectivity options.",
    consumption_value=80.0,   # 80W normal operation
    icon="tv",
    is_default=True,
    peak_consumption=120.0,   # 120W peak brightness/processing
    cycle_duration=3,
    on_duration=3
)
fan: Device = Device(
    name="Ceiling Fan",
    description="An electric fan that provides cooling through air circulation.",
    consumption_value=25.0,   # 25W low speed
    icon="fan",
    is_default=True,
    peak_consumption=60.0,    # 60W high speed
    cycle_duration=2,
    on_duration=2
)
smartphone: Device = Device(
    name="Smartphone Charger",
    description="A mobile device charger with multiple functionalities beyond la simple comunicación.",
    consumption_value=5.0,    # 5W normal charging
    icon="smartphone",
    is_default=True,
    peak_consumption=18.0,    # 18W fast charging
    cycle_duration=1,
    on_duration=1
)

coffeemaker: Device = Device(
    name="Coffee Maker",
    description="A machine used to brew coffee, perfect for homes and offices.",
    consumption_value=800.0,  # 800W brewing
    icon="coffee",
    is_default=True,
    peak_consumption=1000.0,  # 1000W initial heating
    cycle_duration=5,
    on_duration=4
)

wifi: Device = Device(
    name="WiFi Router",
    description="A WiFi router that provides wireless connectivity for various devices.",
    consumption_value=12.0,   # 12W continuous operation
    icon="wifi",
    is_default=True,
    peak_consumption=15.0,    # 15W under heavy load
    cycle_duration=3,
    on_duration=2
)