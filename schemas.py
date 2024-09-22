from pydantic import BaseModel
from typing import Optional

# Pydantic model for Exchange
class ExchangeBase(BaseModel):
    name: str
    description: Optional[str] = None

class ExchangeCreate(ExchangeBase):
    pass

class Exchange(ExchangeBase):
    id: int

    class Config:
        orm_mode = True

# Pydantic model for Instrument
class InstrumentBase(BaseModel):
    symbol: str
    exchange_id: int

class InstrumentCreate(InstrumentBase):
    pass

class Instrument(InstrumentBase):
    id: int

    class Config:
        orm_mode = True

# Pydantic model for Candle
class CandleBase(BaseModel):
    time: str
    instrument_id: int
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float

class CandleCreate(CandleBase):
    pass

class Candle(CandleBase):
    class Config:
        orm_mode = True
