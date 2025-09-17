import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.target_guidance_computer.models import Base

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///data/app.db")

# sqlite needs check_same_thread=False for simple Flask demos
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)

def init_db():
    Base.metadata.create_all(engine)
