from internal_transfer.services import check_user_balance, balance_transfer


def get_create_data(request) -> dict:
    data = request.data.copy()
    login = request.user.login
    currency = data.get('sell_currency')
    sum = data.get('sell_quantity')
    if check_user_balance(login, currency, sum):
        balance_transfer(login, currency, sum, is_plus=False)
        data['owner'] = login
        data['data_status'] = True
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
    return True


def make_transaction(trade):
    if trade.type == 'cript':
        balance_transfer(trade.owner, trade.buy_currency, trade.buy_quantity, is_plus=True)
        balance_transfer(trade.participant, trade.sell_currency, trade.sell_quantity, is_plus=True)
    elif trade.type == 'cash' or trade.type == 'card':
        balance_transfer(trade.participant, trade.sell_currency, trade.sell_quantity, is_plus=True)
    trade.status = 'finished'
    trade.save()


def send_notification(email: str):
    pass
