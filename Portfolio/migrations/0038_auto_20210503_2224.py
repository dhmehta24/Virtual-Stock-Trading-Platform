# Generated by Django 3.1.3 on 2021-05-03 16:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0037_auto_20210503_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_realtime_price',
            name='latest_trading_day',
            field=models.CharField(default=datetime.datetime(2021, 5, 3, 22, 24, 43, 441208), max_length=20, null=True),
        ),
    ]
