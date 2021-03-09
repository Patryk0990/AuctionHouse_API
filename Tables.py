from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, SmallInteger, BigInteger, String, Float, DateTime, Text, func

Base = declarative_base()

class Realms(Base):
    __tablename__ = 'realms'
    id = Column(Integer, primary_key=True)
    connected_realm_id = Column(Integer)
    region_id = Column(SmallInteger)
    name = Column(String(255))

class Regions(Base):
    __tablename__ = 'regions'
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(25))
    shortcut = Column(String(4))

class Auctions(Base):
    __tablename__ = 'auctions'
    id = Column(BigInteger, primary_key=True)
    auction_id = Column(BigInteger)
    quantity = Column(Integer)
    unit_price = Column(BigInteger)
    time_left = Column(String(25))
    bid = Column(BigInteger)
    item_id = Column(BigInteger)
    context = Column(SmallInteger)
    bonus_lists = Column(Text)
    modifiers = Column(Text)
    pet_breed_id = Column(SmallInteger)
    pet_level = Column(SmallInteger)
    pet_quality_id = Column(SmallInteger)
    pet_species_id = Column(Integer)
    connected_realm_id = Column(SmallInteger)
    collect_time = Column(DateTime(timezone=True), server_default=func.now())
    last_collect_time = Column(DateTime(timezone=True), onupdate=func.now())

class TempAuctions(Base):
    __tablename__ = 'temp_auctions'
    id = Column(BigInteger, primary_key=True)
    auction_id = Column(BigInteger)
    quantity = Column(Integer)
    unit_price = Column(BigInteger)
    time_left = Column(String(25))
    bid = Column(BigInteger)
    item_id = Column(BigInteger)
    context = Column(SmallInteger)
    bonus_lists = Column(Text)
    modifiers = Column(Text)
    pet_breed_id = Column(SmallInteger)
    pet_level = Column(SmallInteger)
    pet_quality_id = Column(SmallInteger)
    pet_species_id = Column(Integer)
    connected_realm_id = Column(SmallInteger)
    collect_time = Column(DateTime(timezone=True), server_default=func.now())

class SoldAuctions(Base):
    __tablename__ = 'sold_auctions'
    id = Column(BigInteger, primary_key=True)
    item_id = Column(BigInteger)
    quantity = Column(Integer)
    unit_price = Column(BigInteger)
    connected_realm_id = Column(SmallInteger)
    sell_time = Column(DateTime(timezone=True), server_default=func.now())

class Logs(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    information = Column(String)
    date = Column(DateTime(timezone=True), server_default=func.now())