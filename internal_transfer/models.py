from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime
from django.http import Http404

from trading.utils import get_correct_sum
from .services import check_user_wallet, get_sum_with_commission


class InternalTransfer(models.Model):
    owner = models.CharField(max_length=64, blank=True, null=True)
    currency = models.CharField(max_length=12)
    sum = models.CharField(max_length=32)
    sum_with_commission = models.CharField(max_length=32)
    recipient = models.CharField(max_length=64)
    create_at = models.CharField(default=int(datetime.now().timestamp()), max_length=64, blank=True, null=True)
    security_code = models.CharField(
        max_length=10, 
        blank=True, 
        null=True, 
        validators=[RegexValidator(
            '\d{6,10}', 
            message='Пароль должен быть менее 10 символов и больше 6 символов и содержать только цифры', 
            code='invalid_code')]
            )
    status = models.BooleanField(default=False)
    owner_operation = models.CharField(max_length=12, blank=True, null=True)
    recipient_operation = models.CharField(max_length=12)

    class Meta:
        db_table = 'et_internal_transfer'

    def save(self, *args, **kwargs):
        if check_user_wallet(self.recipient, self.currency):
            correct_sum = get_correct_sum(self.currency, get_sum_with_commission(self.sum, 'internal_transfer'))
            self.sum_with_commission = correct_sum
            super().save(*args, **kwargs)
        else:
            raise Http404
