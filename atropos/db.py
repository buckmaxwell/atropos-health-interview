from sqlmodel import create_engine, SQLModel

DATABASE_URL = "postgresql://postgres:postgres@db:5432/atropos"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)
