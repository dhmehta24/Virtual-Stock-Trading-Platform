# Generated by Django 3.1.3 on 2021-04-08 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0009_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_realtime_price',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
