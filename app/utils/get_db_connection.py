
from sqlmodel import  Session, SQLModel, create_engine, text
from utils.default_devices import refrigerator,lightbulb, tv,fan, coffeemaker, smartphone,wifi
from utils.default_simulation import default_simulation
from utils.default_algorithms import cyclic, active, schedule, vcyclic, cactive, sactive,wactive

from utils.default_electric_meter import default_electric_meter

sqlite_file_name = "data.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def update_existing_simulations(session):
    """
    Update existing simulations to have default values for new time/unit properties.
    This handles migration for databases created before time configuration was added.
    """
    try:
        # Check if any simulation is missing the new properties
        result = session.exec(text("""
            SELECT id FROM Simulation 
            WHERE output_unit IS NULL 
               OR time_unit IS NULL 
               OR time_speed IS NULL
        """)).all()
        
        if result:
            # Update existing simulations with default values
            session.exec(text("""
                UPDATE Simulation 
                SET output_unit = COALESCE(output_unit, 'W'),
                    time_unit = COALESCE(time_unit, 'seconds'),
                    time_speed = COALESCE(time_speed, 1.0),
                    simulation_start_time = COALESCE(simulation_start_time, NULL)
                WHERE output_unit IS NULL 
                   OR time_unit IS NULL 
                   OR time_speed IS NULL
            """))
            session.commit()
            print(f"Updated {len(result)} existing simulations with default time/unit properties")
    except Exception as e:
        # If columns don't exist yet (first time setup), this will fail gracefully
        print(f"Migration check (expected on first run): {e}")
        pass

def get_session():
    with Session(engine) as session:
        yield session

def check_initial_config():
    with Session(engine) as session:
        default_consumption_algorithms = session.exec(text("SELECT * FROM ConsumptionAlgorithm")).first()
        devices_created = session.exec(text("SELECT * FROM Device")).first()
        active_simulation = session.exec(text("SELECT * FROM Simulation WHERE is_active = 1")).first()
        active_electric_meter = session.exec(text("SELECT * FROM ElectricMeter")).first()

        # Check and update existing simulations with missing time/unit properties
        update_existing_simulations(session)

        if default_consumption_algorithms and devices_created and active_simulation and active_electric_meter:
            return True
        else:
            if not default_consumption_algorithms:
                session.add(cyclic)
                session.add(active)
                session.add(schedule)
                session.add(vcyclic)
                session.add(cactive)
                session.add(sactive)
                session.add(wactive)
                session.commit()

            if not devices_created:
                # Asignar el algoritmo (u otros valores por defecto) a cada dispositivo.
                refrigerator.algorithm_id = cyclic.id
                lightbulb.algorithm_id = active.id
                tv.algorithm_id = schedule.id
                fan.algorithm_id = vcyclic.id
                coffeemaker.algorithm_id = cactive.id
                smartphone.algorithm_id = sactive.id
                wifi.algorithm_id = cyclic.id

                # Agregar todos los dispositivos por defecto utilizando una lista.
                default_devices = [
                    refrigerator, 
                    lightbulb,
                    tv,
                    fan,
                    coffeemaker,
                    smartphone,
                    wifi
                ]
                session.add_all(default_devices)
                session.commit()

            if not active_simulation:
                session.add(default_simulation)
                session.commit()

            if not active_electric_meter:
                default_electric_meter.simulation_id = default_simulation.id
                session.add(default_electric_meter)
            
            session.commit()

            return True
        






# def check_initial_config():
#     with Session(engine) as session:
#         default_consumption_algorithms = session.exec(text("SELECT * FROM ConsumptionAlgorithm")).first()
#         devices_created = session.exec(text("SELECT * FROM Device")).first()
#         active_simulation = session.exec(text("SELECT * FROM Simulation WHERE is_active = 1")).first()
#         active_electric_meter = session.exec(text("SELECT * FROM ElectricMeter")).first()
#         if default_consumption_algorithms and devices_created and active_simulation and active_electric_meter:
#             return True
#         else:
#             if not default_consumption_algorithms:
#                 session.add(cyclic)
#                 session.commit()

#             if not devices_created:
#                 refrigerator.algorithm_id = cyclic.id
#                 session.add(refrigerator)
#                 session.commit()
                
#             if not active_simulation:
#                 session.add(default_simulation)
#                 session.commit()

#             if not active_electric_meter:
#                 default_electric_meter.simulation_id = default_simulation.id
#                 session.add(default_electric_meter)

#             session.commit()

#             return True