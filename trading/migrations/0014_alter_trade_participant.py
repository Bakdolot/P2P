# Generated by Django 3.2.9 on 2021-11-11 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0013_alter_trade_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='participant',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Email покупателя'),
        ),
    ]