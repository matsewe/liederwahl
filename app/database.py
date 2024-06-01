from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.types import PickleType

import os

SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.environ.get("DATABASE_URL", "/data/db.sqlite")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, bool]: PickleType,
        object: PickleType,
        set: PickleType
    }