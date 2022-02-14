import requests
from dotenv import load_dotenv
import os
import json

STOCK = "TSLA"


class Stock:

    def __init__(self, stock=None):

        if stock is None:
            self.stock = STOCK
        else:
            self.stock = stock

        load_dotenv("C:/env/.env.txt")
        self.apikey = os.getenv("api_key_stock")

    def change(self):
        changed = None

        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={self.stock}&apikey={self.apikey}'
        r = requests.get(url)
        data = r.json()

        with open(f"{self.stock}.json", "w") as f:
            json.dump(data, f)
        if abs(float(data["Global Quote"]["10. change percent"].rstrip("%"))) >= 2:
            if changed is None:
                changed = float(data["Global Quote"]["10. change percent"].rstrip("%"))
            else:
                changed = float(data["Global Quote"]["10. change percent"].rstrip("%"))

        return changed

