from decimal import Decimal
from .models import EtBalance, EtAuthTokens, EtCurrency, TradeCript


def get_login(token: str) -> str:
    user = EtAuthTokens.objects.get(token=token)
    return user.login


def checking_and_debiting_balance(login: str, quantity: Decimal, currency: int) -> bool:
    """ Проверка баланса, если на балансе достаточно средств - они
        списываются со счета, в противном случае сделка не может быть создана
    """
    try:
        currency = EtCurrency.objects.get(id=currency)
        balance = EtBalance.objects.get(login=login, currency=currency.alias)
        if Decimal(balance.balance) >= Decimal(quantity):
            balance.balance = str(Decimal(balance.balance) - Decimal(quantity))
            balance.save(update_fields=['balance'])
            return True
    except Exception as e:
        print(e)
        return False

    return False


def make_transaction(trade) -> bool:
    sell_currency =  EtCurrency.objects.get(id=trade.sell_currency)
    buy_currency = EtCurrency.objects.get(id=trade.buy_currency)
    owner_balance = EtBalance.objects.get(login=trade.owner, currency=buy_currency.alias)
    participant_balance = EtBalance.objects.get(login=trade.participant, currency=sell_currency.alias)
    owner_cur_balance = Decimal(owner_balance.balance)
    owner_balance.balance = owner_cur_balance + Decimal(trade.buy_quantity)
    participant_cur_balance = Decimal(participant_balance.balance)
    participant_balance.balance = participant_cur_balance + Decimal(trade.sell_quantity)
    owner_balance.save()
    participant_balance.save()
    trade.is_paid = True
    trade.save()
    return True


def send_notification(id: str):
    pass
