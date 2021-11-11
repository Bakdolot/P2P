from decimal import Decimal
from django.db import transaction

from .models import EtBalance, EtAuthTokens, EtCurrency, EtParameters
from .utils import get_commission


def get_login(token: str) -> str:
    user = EtAuthTokens.objects.get(token=token)
    return user.login


def checking_and_debiting_balance(login: str, quantity: str, currency: int) -> bool:
    """ Проверка баланса, если на балансе достаточно средств - они
        списываются со счета, в противном случае сделка не может быть создана
    """
    try:
        with transaction.atomic():
            currency = EtCurrency.objects.get(id=currency)
            balance = EtBalance.objects.get(login=login, currency=currency.alias)

            if Decimal(balance.balance) >= Decimal(quantity):
                balance.balance = str(Decimal(balance.balance) - Decimal(quantity))
                balance.save(update_fields=['balance'])
                return True
    except Exception as e:
        return False

    return False


def make_transaction(trade) -> bool:
    try:
        with transaction.atomic():
            commission = EtParameters.objects.get(categories='otc', alias='commission')
            if trade.type == 'cript':  # Крипта
                sell_currency = EtCurrency.objects.get(id=trade.sell_currency)
                buy_currency = EtCurrency.objects.get(id=trade.buy_currency)

                owner = EtBalance.objects.get(login=trade.owner, currency=buy_currency.alias)
                participant = EtBalance.objects.get(login=trade.participant, currency=sell_currency.alias)

                owner.balance = str(Decimal(owner.balance) + Decimal(trade.buy_quantity))
                participant.balance = str(Decimal(participant.balance) + Decimal(get_commission(
                    trade.sell_quantity, commission.value)))

                owner.save()
                participant.save()

                trade.status = 'finished'
                trade.is_active = False
                trade.save()
                return True

            elif trade.type == 'card':  # Карта
                sell_currency = EtCurrency.objects.get(id=trade.sell_currency)

                participant = EtBalance.objects.get(login=trade.participant, currency=sell_currency.alias)

                participant.balance = str(Decimal(participant.balance) + Decimal(trade.sell_quantity))
                participant.save()

                trade.status = 'finished'
                trade.save()
                return True

    except Exception as e:
        print(e)
        return False


def send_notification(email: str):
    pass


