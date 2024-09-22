from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

# Exchange model
class Exchange(Base):
    __tablename__ = 'exchange'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    instruments = relationship('Instrument', back_populates='exchange')

# Instrument model
class Instrument(Base):
    __tablename__ = 'instrument'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, nullable=False)
    exchange_id = Column(Integer, ForeignKey('exchange.id'), nullable=False)

    exchange = relationship('Exchange', back_populates='instruments')
    candles = relationship('Candle', back_populates='instrument')

# Candle model
class Candle(Base):
    __tablename__ = 'candles'

    time = Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    instrument_id = Column(Integer, ForeignKey('instrument.id'), primary_key=True, nullable=False)
    timeframe = Column(String, primary_key=True, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    instrument = relationship('Instrument', back_populates='candles')
