# Generated by Django 3.1.3 on 2021-04-21 12:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0034_auto_20210419_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_realtime_price',
            name='latest_trading_day',
            field=models.CharField(default=datetime.datetime(2021, 4, 21, 17, 57, 8, 969955), max_length=20),
        ),
    ]
