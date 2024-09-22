import os
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import psycopg2
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.database import AsyncSessionLocal, Base
from db.models import Exchange, Instrument, Candle

app = FastAPI()

# Create a hypertable for the candles table
def create_hypertable():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST")
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT create_hypertable('candles', 'time', if_not_exists => TRUE);
    """)
    conn.commit()
    cursor.close()
    conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the hypertable when the app starts
    create_hypertable()
    
    yield
    
    # Cleanup tasks can be done here (if any)

app = FastAPI(lifespan=lifespan)

# Dependency for database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# @app.get("/exchanges/", response_model=list[Exchange])
# async def list_exchanges(session: AsyncSession = Depends(get_db)):
#     result = await session.execute(select(Exchange))
#     return result.scalars().all()

# @app.post("/exchanges/", response_model=Exchange)
# async def create_exchange(exchange: Exchange, session: AsyncSession = Depends(get_db)):
#     await Exchange.create(session, **exchange.__dict__)
#     return exchange

# @app.get("/instruments/", response_model=list[Instrument])
# async def list_instruments(session: AsyncSession = Depends(get_db)):
#     result = await session.execute(select(Instrument))
#     return result.scalars().all()

# @app.post("/instruments/", response_model=Instrument)
# async def create_instrument(instrument: Instrument, session: AsyncSession = Depends(get_db)):
#     await Instrument.create(session, **instrument.__dict__)
#     return instrument
