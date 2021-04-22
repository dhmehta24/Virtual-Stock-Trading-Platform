# Generated by Django 3.1.3 on 2021-04-15 04:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Portfolio', '0022_investor_staus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investor_staus',
            name='investor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='investor_staus',
            name='loss',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='investor_staus',
            name='n_transactions',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='investor_staus',
            name='p_transactions',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='investor_staus',
            name='profit',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='investor_staus',
            name='transactions',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
