# Generated by Django 3.2.9 on 2021-11-09 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0005_trade_is_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeCash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=150, verbose_name='login')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('sell_currency', models.IntegerField(blank=True, verbose_name='ID валюты (фиат)')),
                ('buy_currency', models.IntegerField(blank=True, verbose_name='ID покупаемой крипты')),
                ('buy_quantity', models.DecimalField(decimal_places=10, max_digits=19, verbose_name='Сумма валюты (фиат)')),
                ('sell_quantity', models.DecimalField(decimal_places=10, max_digits=19, verbose_name='Сумма продаваемой крипты')),
                ('description', models.TextField(verbose_name='Описание')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('participant', models.CharField(blank=True, max_length=150, verbose_name='Email покупателя')),
                ('status', models.BooleanField(default=False, verbose_name='Статус сделки')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Долгота')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Широта')),
            ],
            options={
                'db_table': 'et_trade_cash',
            },
        ),
        migrations.CreateModel(
            name='TradeCript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=150, verbose_name='Email продавца')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('sell_currency', models.IntegerField(blank=True, verbose_name='ID продаваемой крипты')),
                ('buy_currency', models.IntegerField(blank=True, verbose_name='ID покупаемой крипты')),
                ('sell_quantity', models.DecimalField(decimal_places=10, max_digits=19, verbose_name='Сумма продаваемой крипты')),
                ('buy_quantity', models.DecimalField(decimal_places=10, max_digits=19, verbose_name='Сумма покупаемой крипты')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('participant', models.CharField(blank=True, max_length=150, verbose_name='Email покупателя')),
                ('status', models.BooleanField(default=False, verbose_name='Статус сделки')),
            ],
            options={
                'db_table': 'et_trade_cript',
            },
        ),
        migrations.DeleteModel(
            name='Trade',
        ),
    ]
