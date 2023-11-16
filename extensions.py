import requests
import json
import config

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException("Вы пытаетесь перевести валюту саму в себя.")

        try:
            base = base.upper()
            quote = quote.upper()
            amount = float(amount)
        except ValueError:
            raise APIException("Пожалуйста, введите правильное число в поле количество.")

        url = f"https://api.exchangerate-api.com/v4/latest/{base}"
        response = requests.get(url)
        data = json.loads(response.text)

        if "error" in data:
            raise APIException(data["error"])

        conversion_rate = data["rates"][quote]
        converted_amount = amount * conversion_rate

        return converted_amount