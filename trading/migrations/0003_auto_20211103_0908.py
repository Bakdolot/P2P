# Generated by Django 3.2.9 on 2021-11-03 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0002_auto_20211103_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='participant',
            field=models.CharField(blank=True, max_length=150, verbose_name='Токен покупателя'),
        ),
    ]
