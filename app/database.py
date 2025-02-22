from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///db.sqlite3"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables():
  SQLModel.metadata.create_all(engine)


def get_session():
  with Session(engine) as session:
    yield session
