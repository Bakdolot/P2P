# Generated by Django 3.2.9 on 2021-11-22 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('api_id', models.IntegerField()),
                ('logo', models.ImageField(upload_to='Pay24/')),
                ('order_id', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'et_pay24_categories',
            },
        ),
        migrations.CreateModel(
            name='Pay24Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField()),
                ('service', models.IntegerField()),
                ('login', models.CharField(max_length=64)),
                ('operation_type', models.SmallIntegerField()),
                ('sum', models.CharField(max_length=32)),
                ('currency', models.CharField(max_length=12)),
                ('guid', models.CharField(blank=True, max_length=120, null=True)),
                ('ip_address', models.CharField(max_length=32)),
                ('date_creation', models.CharField(blank=True, default=1637578130.305024, max_length=32, null=True)),
                ('date_update', models.CharField(blank=True, max_length=32, null=True)),
                ('commission', models.CharField(blank=True, max_length=12, null=True)),
            ],
            options={
                'db_table': 'et_pay24_operations',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('api_id', models.IntegerField()),
                ('order_id', models.SmallIntegerField()),
            ],
            options={
                'db_table': 'et_pay24_services',
            },
        ),
    ]