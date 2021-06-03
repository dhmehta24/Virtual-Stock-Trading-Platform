# Generated by Django 3.1.3 on 2021-04-14 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_investor_phone'),
        ('Portfolio', '0021_auto_20210413_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investor_Staus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=500000)),
                ('transactions', models.PositiveIntegerField()),
                ('profit', models.PositiveIntegerField()),
                ('loss', models.IntegerField()),
                ('p_transactions', models.PositiveIntegerField()),
                ('n_transactions', models.PositiveIntegerField()),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.investor')),
            ],
        ),
    ]