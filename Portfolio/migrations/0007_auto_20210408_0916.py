# Generated by Django 3.1.3 on 2021-04-08 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0006_daily_realtime_price_market'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_realtime_price',
            name='company_ticker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Portfolio.company_names'),
        ),
    ]
