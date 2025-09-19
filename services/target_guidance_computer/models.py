"""
SQLAlchemy ORM models for Messier Target Guidance Computer.

Defines the TgcAccount table for user accounts and tracking Messier progress.
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column, BigInteger, Index, Integer, String, DateTime, Text, Float,
    func, UniqueConstraint, text
)

Base = declarative_base()

class TgcAccount(Base):
    """
    ORM model for the tgc_account table.

    Stores user account info, location, Bortle score, Messier progress, and timestamps.

    Attributes:
        id (int): Primary key, auto-incremented.
        room_name (str): User's room name identifier.
        country (str): Country code.
        zipcode (str): Zip code.
        passphrase (str): Hashed passphrase.
        latitude (float): Latitude of user's location.
        longitude (float): Longitude of user's location.
        bortle (str): Bortle scale value (1-9), nullable until provided.
        seen_list (str): Comma-separated Messier numbers seen.
        created_at (datetime): Account creation timestamp.
        last_login_at (datetime): Last login timestamp.
        run_counter (int): Number of times the user has run the guidance computer.
    """
    __tablename__ = "tgc_account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(64), nullable=False)
    country   = Column(String(64), nullable=False)
    zipcode   = Column(String(16), nullable=False)
    passphrase = Column(String(255), nullable=False)
    latitude  = Column(Float)   # Latitude as float
    longitude = Column(Float)   # Longitude as float
    bortle    = Column(String(2))    # Bortle scale (1-9), nullable
    seen_list = Column(Text)         # Comma-separated Messier numbers
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),                 # SQLAlchemy-side default
        server_default=text("CURRENT_TIMESTAMP")  # DB-side default
    )
    last_login_at = Column(DateTime, nullable=True)
    run_counter = Column(Integer, default=0, nullable=False) 

    __table_args__ = (
        UniqueConstraint("room_name", "country", "zipcode", name="uq_room_location"),
    )


class GeocodeCache(Base):
    __tablename__ = "geocode_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(2), nullable=False, index=True)
    zipcode = Column(String(10), nullable=False, index=True)
    latitude = Column(Float, nullable=True)  # None if geocoding failed
    longitude = Column(Float, nullable=True)  # None if geocoding failed
    cached_at = Column(DateTime, default=func.now())
    
    # Composite unique constraint to prevent duplicate entries
    __table_args__ = (
        Index('idx_country_zipcode', 'country', 'zipcode'),
    )