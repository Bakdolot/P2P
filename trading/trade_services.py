import requests

from decimal import Decimal
from models import EtBalance, EtAuthTokens


def checking_and_debiting_balance(token: str, quantity: Decimal, currency: int) -> bool:
    """ Проверка баланса, если на балансе достаточно средств - они
        списываются со счета, в противном случае сделка не может быть создана
    """
    try:
        login = EtAuthTokens.objects.get(token=token)
        balance = EtBalance.objects.get(login=login.login, currency=currency)

        if Decimal(balance.balance) < quantity:
            balance.balance -= quantity
            balance.save(update_fields=['balance'])
            return True
        return False

    except Exception as e:
        return False


def make_transaction(owner: str, participant: str, sell: int, buy: int, quantity: int) -> int:
    url = 'some url'
    response = requests.post(url, headers={'Authorization': 'Basic *******'},
                             data={'owner': owner, 'quantity': quantity,
                                   'sell': sell, 'participant': participant,
                                   'buy': buy},)
    return response.status_code


def send_notification(id: str):
    pass
