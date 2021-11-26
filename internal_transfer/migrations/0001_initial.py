# Generated by Django 3.2.9 on 2021-11-16 09:20

from django.db import migrations, models
import unixtimestampfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InternalTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=64)),
                ('currency', models.CharField(max_length=12)),
                ('sum', models.CharField(max_length=32)),
                ('sum_with_commission', models.CharField(max_length=32)),
                ('recipient', models.CharField(max_length=64)),
                ('create_at', unixtimestampfield.fields.UnixTimeStampField(auto_now_add=True)),
                ('security_code', models.CharField(blank=True, max_length=15, null=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
    ]