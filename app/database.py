import os
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    DateTime,
    JSON,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Create SQLite database in the project directory
DATABASE_URL = f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), '../', 'pixelbar.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database models
class FlashMessage(Base):
    __tablename__ = "flash_messages"

    uuid = Column(String, primary_key=True, index=True)
    screen_id = Column(String, index=True)
    message = Column(String)
    type = Column(String)
    number_of_replays = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.utcnow)


class HotData(Base):
    __tablename__ = "hot_data"

    uuid = Column(String, primary_key=True, index=True)
    sequence_id = Column(Integer)
    widget_id = Column(String, index=True)
    json_data = Column(JSON)
    created = Column(DateTime, default=datetime.utcnow)


# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
