import os
import time
from datetime import datetime
from dotenv import load_dotenv
from amazon_paapi import AmazonApi, AmazonApiException
from ebaysdk.shopping import Connection as Shopping
from sqlalchemy import create_engine, MetaData, Table, insert

# Load environment\load_dotenv()

# Amazon PA-API configuration
amazon = AmazonApi(
    access_key=os.getenv('AWS_ACCESS_KEY_ID'),
    secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    partner_tag=os.getenv('PARTNER_TAG'),
    host='webservices.amazon.it',
    region='eu-west-1'
)

# eBay API configuration
ebay = Shopping(
    domain='open.api.ebay.com',
    appid=os.getenv('EBAY_APP_ID'),
    certid=os.getenv('EBAY_CERT_ID'),
    devid=os.getenv('EBAY_DEV_ID'),
    token=os.getenv('EBAY_OAUTH_TOKEN'),
    config_file=None
)

# Database setup
DB_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DB_URL)
metadata = MetaData(bind=engine)
prices_table = Table('prices', metadata, autoload_with=engine)

# Function to upsert price record
def upsert_price(record):
    stmt = insert(prices_table).values(**record).on_conflict_do_nothing(
        index_elements=['product_id', 'source', 'ts']
    )
    with engine.begin() as conn:
        conn.execute(stmt)

# Fetch price from Amazon
def get_amazon_price(asin: str) -> dict:
    try:
        response = amazon.get_items(item_ids=[asin])
        item = response.items_result.items[0]
        listing = item.offers.listings[0]
        return {
            'source': 'amazon',
            'product_id': asin,
            'price': float(listing.price.amount),
            'currency': listing.price.currency,
            'ts': datetime.utcnow()
        }
    except AmazonApiException as err:
        print(f"Amazon API error: {err}")
        return {}

# Fetch price from eBay
def get_ebay_price(item_id: str) -> dict:
    try:
        resp = ebay.execute('GetSingleItem', {'ItemID': item_id, 'IncludeSelector': 'Details'})
        item = resp.dict().get('Item', {})
        price = float(item['CurrentPrice']['value'])
        return {
            'source': 'ebay',
            'product_id': item_id,
            'price': price,
            'currency': item['CurrentPrice']['currencyID'],
            'ts': datetime.utcnow()
        }
    except Exception as err:
        print(f"eBay API error: {err}")
        return {}

if __name__ == '__main__':
    # List of products to track
    products = [
        {'source': 'amazon', 'id': 'B0BMZYEY1V'},
        {'source': 'ebay', 'id': '123456789012'}
    ]

    while True:
        for p in products:
            record = get_amazon_price(p['id']) if p['source']=='amazon' else get_ebay_price(p['id'])
            if record:
                upsert_price(record)
                print(f"Inserted: {record}")
            time.sleep(1)
        # Repeat every hour
        time.sleep(3600)
