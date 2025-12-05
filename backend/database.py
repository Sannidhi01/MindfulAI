from sqlmodel import SQLModel, create_engine, Session

# Replace with your actual DB credentials
DB_URL = "mysql+mysqlconnector://root:password@localhost/mental_health_db"
engine = create_engine(DB_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
