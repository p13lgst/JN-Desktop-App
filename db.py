import os

from sqlalchemy import (
    create_engine,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    PickleType,
    String
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Get the declarative base class.
Base = declarative_base()

# Create the engine.
engine = create_engine(open('.db', encoding='utf-8').read())

# Get a sessionmaker, bound the engine.
Session = sessionmaker(bind=engine)


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    orders = relationship("Order")
    payments = relationship("Payment")


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    local = Column(String)
    itens = Column(PickleType)
    total = Column(Numeric)
    extra_info = Column(String)
    delivered = Column(Boolean)
    client_id = Column(Integer, ForeignKey('clients.id'))


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric)
    date = Column(Date)
    client_id = Column(Integer, ForeignKey('clients.id'))


class Iten(Base):
    __tablename__ = 'itens'
    name = Column(String, primary_key=True)
    price = Column(Numeric)


def get_session():
    """Create all the tables and return the session."""
    Base.metadata.create_all(engine)
    return Session()
