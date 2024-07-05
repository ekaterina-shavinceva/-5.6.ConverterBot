import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CurrencyConverter():
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        quote = quote.lower()
        base = base.lower()
        if quote not in keys:
            raise ConvertionException(f'Валюта {quote} не найдена.')

        if base not in keys:
            raise ConvertionException(f'Валюта {base} не найдена.')


        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')



        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
        total_base = json.loads(r.content)[keys[base]]

        return float(total_base * amount)
