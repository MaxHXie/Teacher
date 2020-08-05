# Generated by Django 3.0.8 on 2020-08-05 07:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0009_auto_20200802_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essay',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='essay',
            name='upload_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 5, 7, 8, 4, 150787, tzinfo=utc), verbose_name='date uploaded'),
        ),
    ]