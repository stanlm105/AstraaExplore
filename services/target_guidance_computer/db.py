"""
Database setup and session management for Messier Target Guidance Computer.

Handles SQLAlchemy engine creation, session factory, and database initialization.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.target_guidance_computer.models import Base

# Get database URL from environment or default to local SQLite
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///data/app.db")

# SQLite requires check_same_thread=False for use with Flask's threaded server
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Create SQLAlchemy engine and session factory
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
    connect_args=connect_args
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)

def init_db():
    """
    Initialize the database by creating all tables defined in models.Base.
    Call this once at startup or during migrations.
    """
    Base.metadata.create_all(engine)