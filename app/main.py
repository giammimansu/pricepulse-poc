import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, select

# Load environment
load_dotenv()

# Database configuration
DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DB_URL)
metadata = MetaData()

# Reflect prices table
def get_prices_table():
    return Table('prices', metadata, autoload_with=engine)

# Pydantic model
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

@app.get("/products/{source}/{product_id}/history", response_model=list[PriceRecord])
def get_history(source: str, product_id: str):
    prices_tbl = get_prices_table()
    with engine.connect() as conn:
        stmt = (
            select(prices_tbl)
            .where(prices_tbl.c.source == source, prices_tbl.c.product_id == product_id)
            .order_by(prices_tbl.c.ts.desc())
            .limit(100)
        )
        rows = conn.execute(stmt).fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="No data found")
    return [PriceRecord(**dict(r)) for r in rows]