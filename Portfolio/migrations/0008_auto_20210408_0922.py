# Generated by Django 3.1.3 on 2021-04-08 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0007_auto_20210408_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_realtime_price',
            name='company_ticker',
            field=models.CharField(max_length=50),
        ),
    ]