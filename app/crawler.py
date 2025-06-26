import os
import time
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, insert
from services.amazon_api import get_amazon_price
from services.ebay_api import get_ebay_price
from dotenv import load_dotenv

load_dotenv()

DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DB_URL)
metadata = MetaData(bind=engine)
prices_tbl = Table('prices', metadata, autoload_with=engine)

def upsert_price(rec: dict):
    stmt = insert(prices_tbl).values(**rec).on_conflict_do_nothing(index_elements=['product_id','source','ts'])
    with engine.begin() as conn:
        conn.execute(stmt)

products = [
    {'source':'amazon','id':'B0BMZYEY1V'},
    {'source':'ebay','id':'123456789012'}
]

if __name__ == '__main__':
    while True:
        for p in products:
            if p['source']=='amazon':
                rec = get_amazon_price(p['id'], sandbox=True)
            else:
                rec = get_ebay_price(p['id'])
            if rec:
                upsert_price(rec)
                print("Inserted:", rec)
            time.sleep(1)
        time.sleep(3600)
