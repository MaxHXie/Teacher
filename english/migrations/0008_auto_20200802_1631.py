# Generated by Django 3.0.8 on 2020-08-02 16:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0007_auto_20200802_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essay',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='essay',
            name='upload_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 2, 16, 31, 54, 775323, tzinfo=utc), verbose_name='date uploaded'),
        ),
    ]
