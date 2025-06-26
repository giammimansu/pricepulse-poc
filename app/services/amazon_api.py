import os
from datetime import datetime
from amazon_paapi import AmazonApi, AmazonApiException
from dotenv import load_dotenv

load_dotenv()

def make_amazon_client(sandbox: bool = False):
    if sandbox:
        host   = "webservices-sandbox.amazon.com"
        access = os.getenv("AWS_ACCESS_KEY_ID_SANDBOX")
        secret = os.getenv("AWS_SECRET_ACCESS_KEY_SANDBOX")
        tag    = os.getenv("PARTNER_TAG_SANDBOX")
    else:
        host   = "webservices.amazon.it"
        access = os.getenv("AWS_ACCESS_KEY_ID")
        secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        tag    = os.getenv("PARTNER_TAG")

    return AmazonApi(
        access_key=access,
        secret_key=secret,
        partner_tag=tag,
        host=host,
        region="eu-west-1"
    )

def get_amazon_price(asin: str, sandbox: bool = False) -> dict:
    client = make_amazon_client(sandbox)
    try:
        resp = client.get_items(item_ids=[asin])
        item = resp.items_result.items[0]
        listing = item.offers.listings[0]
        return {
            "source": "amazon",
            "product_id": asin,
            "price": float(listing.price.amount),
            "currency": listing.price.currency,
            "ts": datetime.utcnow()
        }
    except AmazonApiException as e:
        print(f"[{'SANDBOX' if sandbox else 'PROD'}] Amazon API error: {e}")
        return {}
