from django.db import transaction

from .models import EtBalance, EtAuthTokens, EtCurrency, EtParameters
from .utils import get_commission


def get_login(token: str) -> str:
    user = EtAuthTokens.objects.get(token=token)
    return user.login


def get_commission_value():
    return EtParameters.objects.get(categories='otc', alias='commission').value


def checking_and_debiting_balance(login: str, quantity: str, currency: int) -> bool:
    """ Проверка баланса, если на балансе достаточно средств - они
        списываются со счета, в противном случае сделка не может быть создана
    """
    try:
        with transaction.atomic():
            balance = EtBalance.objects.get(login=login, currency=currency)

            if float(balance.balance) >= float(quantity):
                balance.balance = str(float(balance.balance) - float(quantity))
                balance.save(update_fields=['balance'])
                return True
    except Exception as e:
        print(e)
        return False

    return False


def make_transaction(trade) -> bool:
    try:
        with transaction.atomic():

            if trade.type == 'cript':  # Крипта
                owner = EtBalance.objects.get(login=trade.owner, currency=trade.buy_currency)
                participant = EtBalance.objects.get(login=trade.participant, currency=trade.sell_currency)

                owner.balance = str(float(owner.balance) + float(trade.buy_quantity))
                participant.balance = str(float(participant.balance) + float(trade.sell_quantity_with_commission))

                owner.save()
                participant.save()

                trade.status = 'finished'
                trade.is_active = False
                trade.save()
                return True

            elif trade.type == 'card':  # Карта

                participant = EtBalance.objects.get(login=trade.participant, currency=trade.sell_currency)

                participant.balance = str(float(participant.balance) + float(trade.sell_quantity))
                participant.save()

                trade.status = 'finished'
                trade.save()
                return True
            
            elif trade.type == 'cash':
                user = EtBalance.objects.get(login=trade.participant, currency=trade.sell_currency)

                user.balance = str(float(user.balance) + float(trade.sell_quantity))
                trade.status = 'finished'
                
                trade.save()
                user.save()

    except Exception as e:
        print(e)
        return False


def delete_trade(trade):
    with transaction.atomic():
        try:
            owner_balance = EtBalance.objects.get(login=trade.owner, currency=trade.currency)
            owner_balance = str(float(owner_balance.balance) + float(trade.sell_quantity))
            owner_balance.save()
            return True
        except Exception as e:
            return False



def send_notification(email: str):
    pass


