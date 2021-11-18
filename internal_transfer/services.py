from django.db import transaction

from trading.models import EtBalance, EtParameters, EtOperations
import uuid


def get_trade_type(type: str):
    if type == 'block':
        return EtParameters.objects.get(categories='operationType', alias='block')
    elif type == 'exchange':
        return EtParameters.objects.get(categories='operationType', alias='exchange')
    elif type == 'transfer':
        return EtParameters.objects.get(categories='operationType', alias='transfer')


def get_finished_status_value() -> int:
    return EtParameters.objects.get(categories='operationStatus', alias='completed').value


def create_operation(type: str, login: str, method: str, currency: str, sum: str, ip_address: str, transfer_type: str=None, commission: str=None) -> int:
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
        status = get_finished_status_value()
    )
    if op_type.alias == 'exchange':
        operation.credit = sum
    elif op_type.alias == 'block':
        operation.debit = sum
    elif op_type.alias == 'transfer':
        if transfer_type == 'debit':
            operation.debit = sum
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
    ip = get_client_ip(request)
    if check_user_balance(user, data.get('currency'), data.get('sum')):
        balance_transfer(user, data.get('currency'), data.get('sum'), is_plus=False)
        operation_id = create_operation('block', user, 'internal transfer', data.get('currency'), data.get('sum'), ip)
        data['owner_operation'] = operation_id
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
        operation = EtOperations.objects.get(operation_id=transfer.owner_operation)
        operation.currency = currency
        operation.sum = sum
        operation.save()
    return True


def transfer_data(transfer, request) -> bool:
    if check_user_wallet(transfer.recipient, transfer.currency):
        ip = EtOperations.objects.get(operation_id=transfer.owner).ip_address
        balance_transfer(transfer.recipient, transfer.currency, transfer.sum_with_commission, is_plus=True)
        operation = create_operation('transfer', transfer.recipient, 'internal transfer', transfer.currency, transfer.sum, ip)
        transfer.recipient_operation = operation
        transfer.status = True
        transfer.save()
        return True
    return False
