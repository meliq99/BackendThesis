
from sqlmodel import  Session, SQLModel, create_engine, text
from utils.default_devices import refrigerator, lightbulb
from utils.default_simulation import default_simulation
from utils.default_algorithms import cyclic

from utils.default_electric_meter import default_electric_meter

sqlite_file_name = "data.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def check_initial_config():
    with Session(engine) as session:
        default_consumption_algorithms = session.exec(text("SELECT * FROM ConsumptionAlgorithm")).first()
        devices_created = session.exec(text("SELECT * FROM Device")).first()
        active_simulation = session.exec(text("SELECT * FROM Simulation WHERE is_active = 1")).first()
        active_electric_meter = session.exec(text("SELECT * FROM ElectricMeter")).first()
        if default_consumption_algorithms and devices_created and active_simulation and active_electric_meter:
            return True
        else:
            if not default_consumption_algorithms:
                session.add(cyclic)
                session.commit()

            if not devices_created:
                refrigerator.algorithm_id = cyclic.id
                session.add(refrigerator)
                session.commit()
                
            if not active_simulation:
                session.add(default_simulation)
                session.commit()

            if not active_electric_meter:
                default_electric_meter.simulation_id = default_simulation.id
                session.add(default_electric_meter)

            session.commit()

            return True


    