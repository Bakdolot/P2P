# Generated by Django 3.2.9 on 2021-11-22 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internal_transfer', '0004_auto_20211122_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internaltransfer',
            name='create_at',
            field=models.CharField(blank=True, default=1637578130.303536, max_length=64, null=True),
        ),
    ]