# Generated by Django 3.2.9 on 2021-11-10 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0009_trade_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='status',
            field=models.CharField(choices=[('1', 'in anticipation'), ('2', 'in processing'), ('3', 'finished')], max_length=30, verbose_name='Статус сделки'),
        ),
    ]
