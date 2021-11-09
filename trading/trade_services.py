from decimal import Decimal
from .models import EtBalance, EtAuthTokens, EtCurrency


def get_login(token: str) -> str:
    user = EtAuthTokens.objects.get(token=token)
    return user.login


def checking_and_debiting_balance(login: str, quantity: Decimal, currency: int) -> bool:
    """ Проверка баланса, если на балансе достаточно средств - они
        списываются со счета, в противном случае сделка не может быть создана
    """
    currency = EtCurrency.objects.get(id=currency)

    try:
        balance = EtBalance.objects.get(login=login, currency=currency.alias)
        if Decimal(balance.balance) >= Decimal(quantity):
            balance.balance = str(Decimal(balance.balance) - Decimal(quantity))
            balance.save(update_fields=['balance'])
            return True
    except Exception as e:
        print(e)
        return False

    return False


def make_transaction(owner: str, participant: str, sell: int, buy: int, quantity: int) -> int:

    return None


def send_notification(id: str):
    pass
