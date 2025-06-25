
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, String, Numeric, DateTime, select
import os
from dotenv import load_dotenv

# Load environment variables\load_dotenv()

# Database URL
DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DB_URL)
metadata = MetaData(bind=engine)

# Reflect prices table
def get_prices_table():
    return Table('prices', metadata, autoload_with=engine)

# Pydantic model for price record
class PriceRecord(BaseModel):
    product_id: str
    source: str
    price: float
    currency: str
    ts: datetime

# FastAPI app
app = FastAPI(title="PricePulse POC")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products/{source}/{product_id}/history", response_model=List[PriceRecord])
def get_history(source: str, product_id: str):
    prices = get_prices_table()
    with engine.connect() as conn:
        stmt = select(prices).where(
            prices.c.source == source,
            prices.c.product_id == product_id
        ).order_by(prices.c.ts.desc()).limit(100)
        rows = conn.execute(stmt).fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No data found")
        return [PriceRecord(**dict(row)) for row in rows]
