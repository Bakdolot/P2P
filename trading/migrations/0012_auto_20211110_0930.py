# Generated by Django 3.2.9 on 2021-11-10 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0011_auto_20211110_0726'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='owner_confirm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trade',
            name='participant_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='trade',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='participant_images/'),
        ),
    ]
