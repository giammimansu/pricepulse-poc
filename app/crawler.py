import os
import time
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.dialects.postgresql import insert
from services.amazon_api import get_amazon_price
from services.ebay_api import get_ebay_price

# Load environment
load_dotenv()

# Database setup
DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DB_URL)
metadata = MetaData()
prices_table = Table('prices', metadata, autoload_with=engine)

# Upsert helper
def upsert_price(record: dict):
    stmt = insert(prices_table).values(**record).on_conflict_do_nothing(
        index_elements=['product_id', 'source', 'ts']
    )
    with engine.begin() as conn:
        conn.execute(stmt)

# List of products for POC
products = [
    {'source': 'amazon', 'id': 'B0BMZYEY1V'},
    {'source': 'ebay',   'id': '123456789012'},
]

if __name__ == '__main__':
    while True:
        for p in products:
            if p['source'] == 'amazon':
                record = get_amazon_price(p['id'], sandbox=True)
            else:
                record = get_ebay_price(p['id'], sandbox=True)

            if record:
                upsert_price(record)
                print(f"Inserted: {record}")
            time.sleep(1)
        # Repeat every cycle (for testing, può essere ridotto)
        time.sleep(10)
