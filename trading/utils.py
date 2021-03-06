from django.db.models.signals import pre_save
from .models import Trade, EtOperations
from internal_transfer.services import get_sum_with_commission, get_finance
from datetime import datetime


# def convert_sum(sum: str, step_size: str) -> str:
#     if not '1' in step_size.split('.')[1]:
#         return sum.split('.')[0]
#     step_len = len(step_size.split('.')[1].split('1')[0]) + 1
#     if not '.' in sum:
#         return sum+'.'+('0'*step_len)
#     temp = sum.split('.')
#     if len(temp) == 1:
#         sum = temp[0] + '0' * step_len
#         return sum
#     sum_len = len(sum.split('.')[1])
#     if sum_len > step_len:
#         correct_sum = '.'.join([sum.split('.')[0], sum.split('.')[1][:step_len]])   #   потом оптимизирую
#         return correct_sum
#     diferent = step_len - sum_len
#     correct_sum = '.'.join([sum.split('.')[0], sum.split('.')[1]+('0'*diferent)])
#     return correct_sum


def convert_sum(sum: str, step_size: str) -> str:
    sum = sum.replace(',', '.')
    if not '1' in step_size.split('.')[1]:
        return sum.split('.')[0]
    step_len = len(step_size.split('.')[1].split('1')[0]) + 1
    currect_sum = f"%.{step_len}f" % round(float(sum), step_len)
    return currect_sum


def get_correct_sum(currency, sum):
    step_size = get_finance(currency).step_size
    return convert_sum(sum, step_size)


def my_callback(sender, instance, *args, **kwargs):
    sum_commission = get_sum_with_commission(instance.sell_quantity, 'otc')
    instance.sell_quantity_with_commission = get_correct_sum(instance.sell_currency, sum_commission)
    operation = EtOperations.objects.get(operation_id=instance.owner_operation)
    operation.credit = instance.sell_quantity_with_commission
    operation.save()

pre_save.connect(my_callback, sender=Trade)


def convert_unixtime_to_datetime(unixtime: str) -> str:
    return datetime.utcfromtimestamp(float(unixtime)).strftime('%Y/%m/%d %H:%M')
