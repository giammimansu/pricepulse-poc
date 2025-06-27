import os
from datetime import datetime
from amazon_paapi import AmazonApi
from dotenv import load_dotenv

load_dotenv()

def make_amazon_client(sandbox: bool = False):
    if sandbox:
        access = os.getenv("AWS_ACCESS_KEY_ID_SANDBOX")
        secret = os.getenv("AWS_SECRET_ACCESS_KEY_SANDBOX")
        tag    = os.getenv("PARTNER_TAG_SANDBOX")
        country = "IT"
    else:
        access = os.getenv("AWS_ACCESS_KEY_ID")
        secret = os.getenv("AWS_SECRET_ACCESS_KEY")
        tag    = os.getenv("PARTNER_TAG")
        country = "IT"

    return AmazonApi(
        key=access,
        secret=secret,
        tag=tag,
        country=country
    )

def get_amazon_price(asin: str, sandbox: bool = False) -> dict:
    
    client = make_amazon_client(sandbox)
    # Se siamo in sandbox e mancano le chiavi, restituisco dati fake
    if sandbox and not os.getenv("AWS_ACCESS_KEY_ID_SANDBOX"):
        return {
            "source":     "amazon",
            "product_id": asin,
            "price":      199.99,               # prezzo di esempio
            "currency":   "EUR",
            "ts":         datetime.utcnow()
        }
    
    try:
        # Call get_items with ASIN (string or list)
        resp    = client.get_items(asin)
        item    = resp.items_result.items[0]
        listing = item.offers.listings[0]
        return {
            "source":     "amazon",
            "product_id": asin,
            "price":      float(listing.price.amount),
            "currency":   listing.price.currency,
            "ts":         datetime.utcnow()
        }
    except Exception as e:
        print(f"[{'SANDBOX' if sandbox else 'PROD'}] Amazon API error for {asin}: {e}")
        return {}
