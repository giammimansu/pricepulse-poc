import os
from datetime import datetime
from ebaysdk.shopping import Connection as Shopping
from dotenv import load_dotenv

load_dotenv()

def make_ebay_client(sandbox: bool = False):
    if sandbox:
        # stub senza token reale
        return None
    return Shopping(
        domain='open.api.ebay.com',
        appid=os.getenv('EBAY_APP_ID'),
        certid=os.getenv('EBAY_CERT_ID'),
        devid=os.getenv('EBAY_DEV_ID'),
        token=os.getenv('EBAY_OAUTH_TOKEN'),
        config_file=None
    )

def get_ebay_price(item_id: str, sandbox: bool = False) -> dict:
    """
    Fetch price data for a given eBay ItemID.
    In sandbox mode restituisce dati fittizi, altrimenti chiama l'API reale.
    """
    # stub
    if sandbox:
        return {
            'source':     'ebay',
            'product_id': item_id,
            'price':      49.90,            # prezzo di esempio
            'currency':   'EUR',
            'ts':         datetime.utcnow()
        }

    client = make_ebay_client(sandbox=False)
    try:
        resp = client.execute(
            'GetSingleItem',
            {'ItemID': item_id, 'IncludeSelector': 'Details'}
        )
        item = resp.dict().get('Item', {})
        return {
            'source':     'ebay',
            'product_id': item_id,
            'price':      float(item['CurrentPrice']['value']),
            'currency':   item['CurrentPrice']['currencyID'],
            'ts':         datetime.utcnow()
        }
    except Exception as e:
        print(f"[EBAY] API error for ItemID {item_id}: {e}")
        return {}
