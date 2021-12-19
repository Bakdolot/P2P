from django.db import transaction

from trading.models import EtBalance, EtParameters, EtOperations, EtFinances, EtFinanceRates
from .utils import convert_sum
import uuid


def get_finance(currency):
    return EtFinances.objects.filter(currency=currency).first()


def get_correct_sum(currency, sum):
    step_size = get_finance(currency).step_size
    return convert_sum(sum, step_size)


def get_trade_type(type: str):
    if type == 'block':
        return EtParameters.objects.get(categories='operationType', alias='block')
    elif type == 'exchange':
        return EtParameters.objects.get(categories='operationType', alias='exchange')
    elif type == 'transfer':
        return EtParameters.objects.get(categories='operationType', alias='transfer')


def get_finished_status_value() -> int:
    return EtParameters.objects.get(categories='operationStatus', alias='completed').value


def check_min_sum(sum: str, currency: str, type: str) -> bool:
    if type == 'otc':
        min_usdt = EtParameters.objects.get(categories='otc_options', alias='min_sum').value
        max_usdt = EtParameters.objects.get(categories='otc_options', alias='max_sum').value
    elif type == 'internal':
        min_usdt = EtParameters.objects.get(categories='internal_transfer', alias='min_sum').value
        max_usdt = EtParameters.objects.get(categories='internal_transfer', alias='max_sum').value
    if currency == 'USDT':
        return float(sum) >= float(min_usdt) and float(sum) <= float(max_usdt)
    currency_to_usdt = EtFinanceRates.objects.get(currency_f=currency, currency_t='USDT').rate_buy
    currency = (float(sum) * float(currency_to_usdt))
    return currency >= float(min_usdt) and currency <= float(max_usdt)


def create_operation(
    type: str, login: str, method: str, 
    currency: str, sum: str, ip_address: str, 
    sum_with_commission: str=None, 
    transfer_type: str=None, commission: str=None, requisite: str=None
    ) -> int:
    op_type = get_trade_type(type)
    operation = EtOperations.objects.create(
        operation_type = op_type.value,
        guid = uuid.uuid4(),
        login = login,
        method = method,
        currency = currency,
        sum = sum,
        commission = commission,
        ip_address = ip_address,
        status = get_finished_status_value(),
        requisite = requisite
    )
    if transfer_type == 'debit':
        operation.debit = sum_with_commission if sum_with_commission else sum
    elif transfer_type == 'credit':
        operation.credit = sum
    operation.save()
    return operation.operation_id


def get_commission(category: str) -> str:
    return EtParameters.objects.get(categories=category, alias='commission').value


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_user_wallet(login: str, currency: str) -> bool:
    user = EtBalance.objects.filter(login=login, currency=currency)
    return bool(user)


def get_sum_with_commission(sum: str, category: str) -> str:
    commission = float(get_commission(category)) / 100
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


def transfer_data(transfer) -> bool:
    if check_user_wallet(transfer.recipient, transfer.currency):
        ip = EtOperations.objects.get(operation_id=transfer.owner_operation).ip_address
        balance_transfer(transfer.recipient, transfer.currency, transfer.sum_with_commission, is_plus=True)
        currecy_alias = get_finance(transfer.currency).alias
        operation = create_operation(
            'transfer', transfer.recipient, 
            currecy_alias, transfer.currency, 
            transfer.sum, ip, transfer_type='debit', 
            requisite=transfer.recipient,
            commission=get_commission('internal_transfer')
            )
        transfer.recipient_operation = operation
        transfer.status = True
        transfer.save()
        return True
    return False
