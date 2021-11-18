from django.db import transaction

from trading.models import EtBalance, EtParameters


def check_user_wallet(login: str, currency: str) -> bool:
    user = EtBalance.objects.filter(login=login, currency=currency)
    return bool(user)


def get_sum_with_commission(sum: str, category: str) -> str:
    commission = float(EtParameters.objects.get(categories=category, alias='commission').value) / 100
    sum = str(float(sum)-(float(sum)*commission))
    return sum


def check_user_balance(user: str, currency: str, sum: str) -> bool:
    user_balance = EtBalance.objects.filter(login=user, currency=currency)
    if user_balance:
        user_balance = user_balance.first().balance
        if float(user_balance) >= float(sum):
            return True
    return False


def balance_transfer(user: str, currency: str, sum: str, is_plus: bool = True):
    with transaction.atomic():
        user_balance = EtBalance.objects.get(login=user, currency=currency)
        user_balance.balance = str(float(user_balance.balance) + float(sum)) if is_plus else str(float(user_balance.balance) - float(sum))
        user_balance.save()


def get_data(request) -> dict:
    data = request.data
    user = request.user.login
    if check_user_balance(user, data.get('currency'), data.get('sum')):
        balance_transfer(user, data.get('currency'), data.get('sum'), is_plus=False)
        data['owner'] = user
        data['status'] = True
        return data
    data['status'] = False
    return data


def transfer_update(request, transfer) -> bool:
    user_login = transfer.owner
    currency = request.get('currency')
    sum = request.get('sum')
    if not (currency == transfer.currency and sum == transfer.sum):
        if not check_user_balance(user_login, currency, sum):
            return False
        balance_transfer(user_login, transfer.currency, transfer.sum, is_plus=True)
        balance_transfer(user_login, currency, sum, is_plus=False)
    return True


def transfer_data(transfer) -> bool:
    if check_user_wallet(transfer.recipient, transfer.currency):
        balance_transfer(transfer.recipient, transfer.currency, transfer.sum_with_commission, is_plus=True)
        transfer.status = True
        transfer.save()
        return True
    return False
