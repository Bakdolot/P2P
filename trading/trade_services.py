import requests

from decimal import Decimal


def check_balance(id: str, quantity: Decimal) -> int:
    url = 'some url'
    response = requests.get(url, headers={'user': id, 'quantity': quantity})
    return response.status_code


def send_notification(id: str):
    pass
