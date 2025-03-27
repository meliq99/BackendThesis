
from sqlmodel import  Session, SQLModel, create_engine, text
from utils.default_devices import refrigerator
from utils.default_simulation import default_simulation

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
        query = text("SELECT * FROM Device")
        devices_created = session.exec(query).first()
        active_simulation = session.exec(text("SELECT * FROM Simulation WHERE is_active = 1")).first()
        if devices_created and active_simulation:
            return True
        else:
            if not devices_created:
                session.add(refrigerator)
            if not active_simulation:
                session.add(default_simulation)
                electric_meter = ElectricMeter(

                ).add(
                    simulation_id=default_simulation.id,
                )
            session.commit()

            
            return True


    