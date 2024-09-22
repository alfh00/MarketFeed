import psycopg2
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal
import os

app = FastAPI()

# Create database tables using SQLAlchemy
models.Base.metadata.create_all(bind=engine)

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

# Call the hypertable creation after initializing the models
create_hypertable()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Example route to create a new exchange
@app.post("/exchanges/", response_model=schemas.Exchange)
def create_exchange(exchange: schemas.ExchangeCreate, db: Session = Depends(get_db)):
    db_exchange = models.Exchange(**exchange.dict())
    db.add(db_exchange)
    db.commit()
    db.refresh(db_exchange)
    return db_exchange







