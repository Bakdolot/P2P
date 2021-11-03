import requests

from decimal import Decimal


def check_balance(token: str, quantity: Decimal, sell: int) -> int:
    url = 'some url'
    response = requests.get(url, headers={'Authorization': 'Basic *******'},
                            data={'user': token, 'quantity': quantity, 'sell': sell})
    return response.status_code == 200


def debiting_money(token: str, quantity: Decimal, sell: int) -> int:
    url = 'some url'
    response = requests.post(url, headers={'Authorization': 'Basic *******'},
                             data={'user': token, 'quantity': quantity, 'sell': sell},)
    return response.status_code == 200


def make_transaction(owner: str, participant: str, sell: int, buy: int, quantity: int) -> int:
    url = 'some url'
    response = requests.post(url, headers={'Authorization': 'Basic *******'},
                             data={'owner': owner, 'quantity': quantity,
                                   'sell': sell, 'participant': participant,
                                   'buy': buy},)
    return response.status_code


def send_notification(id: str):
    pass
