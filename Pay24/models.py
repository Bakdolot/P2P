from django.db import models
from datetime import datetime
import uuid


class Category(models.Model):
    name = models.CharField(max_length=120)
    api_id = models.IntegerField(unique=True)
    logo = models.ImageField(upload_to='Pay24/', null=True)
    logo_url = models.URLField(null=True)
    order_id = models.SmallIntegerField()

    class Meta:
        db_table = 'et_pay24_categories'


class Service(models.Model):
    name = models.CharField(max_length=255)
    api_id = models.IntegerField()
    logo = models.ImageField(upload_to='Pay24/', null=True)
    logo_url = models.URLField(null=True)
    order_id = models.IntegerField()
    category = models.IntegerField()
    commission = models.CharField(max_length=12)
    min_sum = models.CharField(max_length=12, default='10')
    max_sum = models.CharField(max_length=12, default='10000')
    support_phone = models.CharField(max_length=24, null=True)

    data = models.TextField()

    class Meta:
        db_table = 'et_pay24_services'


class Pay24Operation(models.Model):
    category = models.IntegerField()
    service = models.IntegerField()
    owner = models.CharField(max_length=64)
    operation_type = models.SmallIntegerField()
    sum = models.CharField(max_length=32)
    sum_with_commission = models.CharField(max_length=32)
    currency = models.CharField(max_length=12)
    guid = models.CharField(max_length=120, default=uuid.uuid4(), blank=True, null=True)
    ip_address = models.CharField(max_length=32)
    date_creation = models.CharField(max_length=32, default=int(datetime.now().timestamp()), blank=True, null=True)
    date_update = models.CharField(max_length=32, blank=True, null=True)
    reference = models.IntegerField()

    def save(self, *args, **kwargs):
        self.date_update = int(datetime.now().timestamp())
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'et_pay24_operations'
