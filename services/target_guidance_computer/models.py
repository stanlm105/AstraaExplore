from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Text, func, UniqueConstraint, PrimaryKeyConstraint

Base = declarative_base()

class TgcAccount(Base):
    __tablename__ = "tgc_account"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    room_name = Column(String(64), nullable=False)
    country   = Column(String(64), nullable=False)
    zipcode   = Column(String(16), nullable=False)
    passphrase = Column(String(255), nullable=False)  # store a bcrypt/argon hash
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    last_login_at = Column(DateTime)
    __table_args__ = (UniqueConstraint("room_name","country","zipcode", name="uq_room_location"),)

class TgcSeen(Base):
    __tablename__ = "tgc_seen"
    account_id     = Column(BigInteger, nullable=False)
    catalog        = Column(String(8), nullable=False)      # 'M','NGC'
    catalog_number = Column(Integer,  nullable=False)       # 31, 42, ...
    first_seen_at  = Column(DateTime, nullable=False, server_default=func.now())
    note           = Column(Text)
    __table_args__ = (PrimaryKeyConstraint("account_id","catalog","catalog_number", name="pk_seen"),)
