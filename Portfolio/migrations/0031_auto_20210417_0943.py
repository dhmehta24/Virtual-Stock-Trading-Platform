# Generated by Django 3.1.3 on 2021-04-17 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0030_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='t_type',
            field=models.CharField(choices=[('BUY', 'BUY'), ('SELL', 'SELL')], default='BUY', max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='history',
            name='bought_price',
            field=models.FloatField(default=0),
        ),
    ]
