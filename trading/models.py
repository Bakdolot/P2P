from django.db import models


class Trade(models.Model):
    TYPE_CHOICES = (
        ('1', 'Крипта'),
        ('2', 'Карта'),
        ('3', 'Наличка')
    )

    owner = models.CharField('Токен продавца', max_length=150)
    is_active = models.BooleanField('Активность', default=True)
    sell = models.IntegerField('ID продаваемой крипты', blank=True)
    buy = models.IntegerField('ID покупаемой крипты', blank=True)
    sell_quantity = models.DecimalField('Сумма продаваемой крипты', max_digits=19, decimal_places=10)
    buy_quantity = models.DecimalField('Сумма покупаемой крипты', max_digits=19, decimal_places=10)
    create_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Изменено', auto_now=True)
    participant = models.CharField('Токен покупателя', blank=True, max_length=150)
    type = models.CharField('Тип сделки', choices=TYPE_CHOICES, max_length=30)
