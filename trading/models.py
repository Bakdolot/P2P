from datetime import datetime
from django.db import models


class Trade(models.Model):
    def upload_to(self) -> str:
        return f'participant_images/{self.participant}/'

    TYPE_CHOICES = (
        ('cript', 'Trade With cript'),
        ('cash', 'Trade with cash'),
        ('card', 'Trade with card')
    )
    STATUS_CHOICES = (
        ('expectation', 'expectation'),
        ('process', 'in processing'),
        ('finished', 'finished')
    )

    owner = models.CharField('Email продавца', max_length=150)
    sell_currency = models.CharField('Продаваемая крипта', max_length=12)
    buy_currency = models.CharField('Покупаемая крипта', max_length=12)
    sell_quantity = models.CharField('Сумма продаваемой крипты', max_length=32)
    sell_quantity_with_commission = models.CharField('Сумма продажи с учетом комиссии', max_length=12)
    buy_quantity = models.CharField('Сумма покупаемой крипты', max_length=32)
    create_at = models.CharField(max_length=64, default=int(int(datetime.now().timestamp())), blank=True, null=True)
    updated_at = models.CharField(max_length=64, blank=True, null=True)
    participant = models.CharField('Email покупателя', blank=True, max_length=150, null=True)
    status = models.CharField('Статус сделки', max_length=30, choices=STATUS_CHOICES, default='expectation')
    type = models.CharField('Тип сделки', max_length=10, choices=TYPE_CHOICES)
    description = models.TextField('Описание', blank=True, null=True)
    phone = models.CharField('Телефонный номер', max_length=50, blank=True, null=True)
    longitude = models.CharField('Долгота', max_length=12, blank=True, null=True)
    latitude = models.CharField('Широта', max_length=12, blank=True, null=True)
    bank_card = models.CharField(max_length=16, blank=True, null=True)
    image = models.FileField(blank=True, null=True, upload_to=f'participant_images/')
    owner_confirm = models.BooleanField(default=False, blank=True, null=True)
    participant_sent = models.BooleanField(default=False, blank=True, null=True)
    owner_operation = models.SmallIntegerField()
    participant_operation = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'et_trade'

    def save(self, *args, **kwargs):
        self.updated_at = int(datetime.now().timestamp())
        super().save(*args, **kwargs)


class EtAuthTokens(models.Model):
    token_id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=280)
    login = models.CharField(max_length=32)
    ip_address = models.CharField(max_length=32)
    user_agent = models.CharField(max_length=280)
    browser = models.CharField(max_length=32, blank=True, null=True)
    date_creation = models.CharField(max_length=32)
    date_expiration = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'et_auth_tokens'


class EtBalance(models.Model):
    login = models.CharField(max_length=64)
    balance = models.CharField(max_length=32)
    currency = models.CharField(max_length=12)
    alias = models.CharField(max_length=64)
    address = models.CharField(max_length=120, blank=True, null=True)
    date_update = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'et_balance'


class EtOperations(models.Model):
    operation_id = models.AutoField(primary_key=True)
    operation_type = models.SmallIntegerField()
    guid = models.CharField(max_length=120, blank=True, null=True)
    login = models.CharField(max_length=32)
    method = models.CharField(max_length=32, blank=True, null=True)
    currency = models.CharField(max_length=12, blank=True, null=True)
    sum = models.CharField(max_length=32)
    credit = models.CharField(max_length=32, blank=True, null=True)
    debit = models.CharField(max_length=32, blank=True, null=True)
    commission = models.CharField(max_length=32, blank=True, null=True)
    rate = models.CharField(max_length=12, blank=True, null=True)
    date_creation = models.CharField(max_length=64, default=int(datetime.now().timestamp()), blank=True, null=True)
    date_update = models.CharField(max_length=64, null=True)
    ip_address = models.CharField(max_length=32)
    memo = models.TextField(blank=True, null=True)
    batch = models.CharField(max_length=120, blank=True, null=True)
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'et_operations'
    
    def save(self, *args, **kwargs):
        self.date_update = int(datetime.now().timestamp())
        super().save(*args, **kwargs)


class EtParameters(models.Model):
    categories = models.CharField(max_length=280)
    name = models.CharField(max_length=280)
    alias = models.CharField(max_length=280)
    value = models.CharField(max_length=280)
    sort = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'et_parameters'


class EtUsers(models.Model):
    guid = models.CharField(max_length=120)
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=120)
    firstname = models.CharField(max_length=32, blank=True, null=True)
    lastname = models.CharField(max_length=32, blank=True, null=True)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=32, blank=True, null=True)
    photo = models.CharField(max_length=32, blank=True, null=True)
    date_creation = models.CharField(max_length=32)
    date_update = models.CharField(max_length=32, blank=True, null=True)
    user_group = models.CharField(max_length=16)
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'et_users'
