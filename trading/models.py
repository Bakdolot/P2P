from django.db import models


class Trade(models.Model):
    TYPE_CHOICES = (
        ('1', 'Trade With cript'),
        ('2', 'Trade with cash'),
        ('3', 'Trade with card')
    )

    STATUS_CHOICES = (
        ('1', 'in anticipation'),
        ('2', 'in processing'),
        ('3', 'finished')
    )

    owner = models.CharField('Email продавца', max_length=150)
    is_active = models.BooleanField('Активность', default=True)
    sell_currency = models.IntegerField('ID продаваемой крипты')
    buy_currency = models.IntegerField('ID покупаемой крипты')
    sell_quantity = models.DecimalField('Сумма продаваемой крипты', max_digits=19, decimal_places=10)
    buy_quantity = models.DecimalField('Сумма покупаемой крипты', max_digits=19, decimal_places=10)
    create_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Изменено', auto_now=True)
    participant = models.CharField('Email покупателя', blank=True, max_length=150)
    status = models.CharField('Статус сделки', max_length=30, choices=STATUS_CHOICES, default='1')
    type = models.CharField('Тип сделки', max_length=10, choices=TYPE_CHOICES)
    description = models.TextField('Описание', blank=True, null=True)
    phone = models.CharField('Телефонный номер', max_length=50, blank=True, null=True)
    longitude = models.DecimalField('Долгота', max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        db_table = 'et_trade'


class EtActivations(models.Model):
    guid = models.CharField(max_length=120)
    login = models.CharField(max_length=64)
    code = models.CharField(max_length=16, blank=True, null=True)
    date_creation = models.CharField(max_length=32)
    date_expiration = models.CharField(max_length=32)
    resend_count = models.SmallIntegerField(blank=True, null=True)
    resend_next = models.CharField(max_length=32, blank=True, null=True)
    attempts = models.SmallIntegerField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'et_activations'


class EtAlerts(models.Model):
    name = models.CharField(max_length=280)
    message = models.TextField()
    lang = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'et_alerts'


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


class EtCountries(models.Model):
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'et_countries'


class EtCurrency(models.Model):
    name = models.CharField(max_length=12)
    alias = models.CharField(max_length=12)
    symbol = models.CharField(max_length=12, blank=True, null=True)
    type = models.SmallIntegerField(blank=True, null=True)
    iso_code = models.IntegerField(blank=True, null=True)
    decimal_number_system = models.SmallIntegerField(blank=True, null=True)
    decimal_separator = models.CharField(max_length=8, blank=True, null=True)
    sort = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'et_currency'


class EtFaq(models.Model):
    faq_id = models.AutoField(primary_key=True)
    category = models.SmallIntegerField()
    question = models.CharField(max_length=260)
    answer = models.TextField()
    date_creation = models.CharField(max_length=32, blank=True, null=True)
    date_update = models.CharField(max_length=32, blank=True, null=True)
    sort = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'et_faq'


class EtFinanceRates(models.Model):
    rate_id = models.AutoField(primary_key=True)
    currency_f = models.CharField(max_length=12, blank=True, null=True)
    currency_t = models.CharField(max_length=12, blank=True, null=True)
    rate_buy = models.CharField(max_length=32, blank=True, null=True)
    rate_sell = models.CharField(max_length=32, blank=True, null=True)
    rate_exchange = models.CharField(max_length=32, blank=True, null=True)
    date_update = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'et_finance_rates'


class EtFinanceRequisites(models.Model):
    finance_requisite_id = models.AutoField(primary_key=True)
    finance_id = models.IntegerField(blank=True, null=True)
    alias = models.CharField(max_length=120, blank=True, null=True)
    username = models.CharField(max_length=280)
    password = models.CharField(max_length=280)
    merchant_id = models.CharField(max_length=280)
    api_key = models.CharField(max_length=320)
    private_key = models.TextField()
    secret_key = models.CharField(max_length=320)

    class Meta:
        managed = False
        db_table = 'et_finance_requisites'


class EtFinances(models.Model):
    finance_id = models.AutoField(primary_key=True)
    finance_type = models.SmallIntegerField(blank=True, null=True)
    direction = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=280)
    alias = models.CharField(max_length=280)
    logo = models.CharField(max_length=16, blank=True, null=True)
    currency = models.CharField(max_length=32)
    date_creation = models.CharField(max_length=32)
    date_update = models.CharField(max_length=32)
    balance = models.CharField(max_length=32, blank=True, null=True)
    min_qty = models.CharField(max_length=32)
    max_qty = models.CharField(max_length=32)
    step_size = models.CharField(max_length=32)
    commission = models.CharField(max_length=12, blank=True, null=True)
    addination_fees = models.CharField(max_length=12, blank=True, null=True)
    cashout_fees = models.CharField(max_length=12, blank=True, null=True)
    cashout_status = models.SmallIntegerField(blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    sort = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'et_finances'


class EtForgotten(models.Model):
    guid = models.CharField(max_length=120)
    login = models.CharField(max_length=120)
    date_creation = models.CharField(max_length=32)
    resend_next = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'et_forgotten'


class EtLang(models.Model):
    name = models.CharField(max_length=280)
    iso = models.CharField(max_length=280)
    alias = models.CharField(max_length=280)
    align = models.CharField(max_length=280)
    sort = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'et_lang'


class EtNotifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=32)
    name = models.CharField(max_length=120)
    message = models.TextField()
    date_creation = models.CharField(max_length=32)
    date_update = models.CharField(max_length=32)
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'et_notifications'


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
    date_creation = models.CharField(max_length=32)
    date_update = models.CharField(max_length=32, blank=True, null=True)
    ip_address = models.CharField(max_length=32)
    memo = models.TextField(blank=True, null=True)
    batch = models.CharField(max_length=120, blank=True, null=True)
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'et_operations'


class EtPages(models.Model):
    name = models.CharField(max_length=120)
    alias = models.CharField(max_length=240)
    user_access = models.CharField(max_length=32)
    user_group = models.CharField(max_length=32)
    default_redirect = models.CharField(max_length=32)
    access_ip = models.CharField(max_length=320)
    date_creation = models.CharField(max_length=32)
    date_update = models.CharField(max_length=32)
    lang = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'et_pages'


class EtParameters(models.Model):
    categories = models.CharField(max_length=280)
    name = models.CharField(max_length=280)
    alias = models.CharField(max_length=280)
    value = models.CharField(max_length=280)
    sort = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'et_parameters'


class EtReviews(models.Model):
    login = models.CharField(max_length=32)
    firstname = models.CharField(max_length=32)
    lastname = models.CharField(max_length=32)
    description = models.TextField()
    date_creation = models.CharField(max_length=32)
    status = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'et_reviews'


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


class EtUsersAction(models.Model):
    login = models.CharField(max_length=64)
    action = models.SmallIntegerField()
    date_creation = models.CharField(max_length=32)
    country = models.CharField(max_length=32)
    ip_address = models.CharField(max_length=32)
    user_browser = models.CharField(max_length=32)
    user_agent = models.CharField(max_length=320)
    screen_resolution = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'et_users_action'


class EtUsersGroup(models.Model):
    name = models.CharField(max_length=32)
    alias = models.CharField(max_length=64)
    redirect = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'et_users_group'


class EtUsersOnline(models.Model):
    session_id = models.AutoField(primary_key=True)
    guid = models.CharField(max_length=120)
    login = models.CharField(max_length=32, blank=True, null=True)
    date_update = models.CharField(max_length=32, blank=True, null=True)
    date_expire = models.CharField(max_length=32)
    user_agent = models.CharField(max_length=320)
    ip_address = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'et_users_online'
