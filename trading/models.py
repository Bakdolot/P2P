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
    quantity = models.DecimalField('Сумма', max_digits=19, decimal_places=2)
    create_at = models.DateTimeField('Дата создания', auto_now_add=True)
    participant = models.CharField('Токен покупателя', blank=True, max_length=150)
    type = models.CharField('Тип', choices=TYPE_CHOICES, max_length=30)
