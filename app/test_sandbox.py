from services.amazon_api import get_amazon_price
from services.ebay_api    import get_ebay_price

def main():
    asin    = "B0BMZYEY1V"
    item_id = "123456789012"

    print("→ Amazon PA-API sandbox:")
    print(get_amazon_price(asin, sandbox=True))

    print("\n→ eBay Shopping API sandbox:")
    print(get_ebay_price(item_id, sandbox=True))

if __name__ == "__main__":
    main()
