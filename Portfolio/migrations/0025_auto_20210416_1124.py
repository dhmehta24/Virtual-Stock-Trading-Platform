# Generated by Django 3.1.3 on 2021-04-16 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0024_holdings_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holdings',
            name='time',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
