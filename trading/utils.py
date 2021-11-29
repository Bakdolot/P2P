from django.db.models.signals import pre_save
from .models import Trade
from internal_transfer.services import get_sum_with_commission
from datetime import datetime


def my_callback(sender, instance, *args, **kwargs):
    instance.sell_quantity_with_commission = get_sum_with_commission(instance.sell_quantity, 'otc')

pre_save.connect(my_callback, sender=Trade)


def convert_unixtime_to_datetime(unixtime: str) -> str:
    return datetime.utcfromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
