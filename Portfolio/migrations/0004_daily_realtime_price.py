# Generated by Django 3.1.3 on 2021-04-06 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0003_company_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily_Realtime_Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_ticker', models.CharField(max_length=50)),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField(null=True)),
                ('price', models.FloatField()),
                ('volume', models.FloatField()),
                ('latest_trading_day', models.DateField()),
                ('prev_close', models.FloatField()),
                ('change', models.FloatField()),
                ('change_percentage', models.TextField()),
            ],
        ),
    ]
