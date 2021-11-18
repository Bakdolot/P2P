from django.db import models
from django.core.validators import RegexValidator
from unixtimestampfield.fields import UnixTimeStampField
from django.http import Http404
from .services import check_user_wallet, get_sum_with_commission


class InternalTransfer(models.Model):
    owner = models.CharField(max_length=64)
    currency = models.CharField(max_length=12)
    sum = models.CharField(max_length=32)
    sum_with_commission = models.CharField(max_length=32)
    recipient = models.CharField(max_length=64)
    create_at = UnixTimeStampField(auto_now_add=True)
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
    owner_operation = models.CharField(max_length=12)
    recipient_operation = models.CharField(max_length=12)

    def save(self, *args, **kwargs):
        if check_user_wallet(self.recipient, self.currency):
            self.sum_with_commission = get_sum_with_commission(self.sum, 'internal_transfer')
            super().save(*args, **kwargs)
        else:
            raise Http404
