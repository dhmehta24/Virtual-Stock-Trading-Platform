# Generated by Django 3.1.3 on 2021-04-13 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portfolio', '0019_auto_20210412_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holdings',
            name='ltp',
            field=models.FloatField(),
        ),
    ]