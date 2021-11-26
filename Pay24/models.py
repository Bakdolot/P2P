from django.db import models
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=120)
    api_id = models.IntegerField()
    logo = models.ImageField(upload_to='Pay24/')
    order_id = models.SmallIntegerField()

    class Meta:
        db_table = 'et_pay24_categories'


class Service(models.Model):
    name = models.CharField(max_length=120)
    api_id = models.IntegerField()
    logo = models.ImageField(upload_to='Pay24/')
    order_id = models.SmallIntegerField()
    category = models.SmallIntegerField()
    commission = models.CharField(max_length=12)
    min_sum = models.CharField(max_length=12)
    max_sum = models.CharField(max_length=12)
    support_phone = models.CharField(max_length=24)

    class Meta:
        db_table = 'et_pay24_services'


class Pay24Operation(models.Model):
    category = models.IntegerField()
    service = models.IntegerField()
    login = models.CharField(max_length=64)
    operation_type = models.SmallIntegerField()
    sum = models.CharField(max_length=32)
    sum_with_commission = models.CharField(max_length=32)
    currency = models.CharField(max_length=12)
    guid = models.CharField(max_length=120, blank=True, null=True)
    ip_address = models.CharField(max_length=32)
    date_creation = models.CharField(max_length=32, default=datetime.now().timestamp(), blank=True, null=True)
    date_update = models.CharField(max_length=32, blank=True, null=True)
    reference = models.IntegerField()

    def save(self, *args, **kwargs):
        self.date_update = datetime.now().timestamp()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'et_pay24_operations'