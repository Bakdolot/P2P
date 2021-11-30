from internal_transfer.services import check_user_balance, balance_transfer, get_client_ip, get_commission, create_operation
from .models import EtOperations


def get_create_data(request) -> dict:
    data = request.data.copy()
    login = request.user.login
    currency = data.get('sell_currency')
    sum = data.get('sell_quantity')
    ip = get_client_ip(request)
    if check_user_balance(login, currency, sum):
        balance_transfer(login, currency, sum, is_plus=False)
        operation_id = create_operation(
            'block', login, 'otc', currency, 
            sum, ip, transfer_type='credit', 
            commission=get_commission('otc')
            )
        data['owner'] = login
        data['data_status'] = True
        data['owner_operation'] = operation_id
        return data
    data['data_status'] = False
    return data


def trade_update(request, trade) -> bool:
    user_login = trade.owner
    currency = request.get('sell_currency')
    sum = request.get('sell_quantity')
    if not (currency == trade.sell_currency and sum == trade.sell_quantity):
        if not check_user_balance(user_login, currency, sum):
            return False
        balance_transfer(user_login, trade.sell_currency, trade.sell_quantity, is_plus=True)
        balance_transfer(user_login, currency, sum, is_plus=False)
        operation = EtOperations.objects.get(id=trade.owner_operation)
        operation.currency = currency
        operation.sum = sum
        operation.save()
    return True


def make_transaction(trade, request):
    ip_recipient = get_client_ip(request)
    if trade.type == 'cript':
        balance_transfer(trade.owner, trade.buy_currency, trade.buy_quantity, is_plus=True)
        balance_transfer(trade.participant, trade.sell_currency, trade.sell_quantity, is_plus=False)
        balance_transfer(trade.participant, trade.sell_currency, trade.sell_quantity_with_commission, is_plus=True)

        ip_ownner = EtOperations.objects.get(operation_id=trade.owner_operation).ip_address
        create_operation(
            'exchange', trade.owner, 'otc', 
            trade.buy_currency, trade.buy_quantity, 
            ip_ownner, transfer_type='debit', 
            commission=get_commission('otc')
            )
        
        operation = create_operation(
            'exchange', trade.participant, 'otc', 
            trade.sell_currency, trade.sell_quantity, 
            ip_recipient, trade.sell_quantity_with_commission, 
            'debit', get_commission('otc')
            )
    elif trade.type == 'cash' or trade.type == 'card':
        balance_transfer(trade.participant, trade.sell_currency, trade.sell_quantity_with_commission, is_plus=True)
        operation = create_operation(
            'exchange', trade.participant, 'otc', 
            trade.sell_currency, trade.sell_quantity,
            ip_recipient, trade.sell_quantity_with_commission, 
            'debit', get_commission('otc')
            )
    trade.status = 'finished'
    trade.participant_operation = operation
    trade.save()
    

def send_notification(email: str):
    pass
