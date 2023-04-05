import json

import requests

from config import keys


class CustomException(Exception):
    pass


class CustomConvertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise CustomException(f'Error. Currencies is equals - {base} ')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise CustomException(f'Incorrect currency: {quote}\n/values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise CustomException(f'Incorrect currency: {base}\n/values')

        try:
            amount = float(amount)
        except ValueError:
            raise CustomException(f'Incorrect amount: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        total_base = json.loads(r.content)[keys[base]]

        return total_base
