# Generated by Django 3.0.8 on 2020-08-02 16:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0008_auto_20200802_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='essay',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='essay',
            name='upload_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 2, 16, 33, 0, 193688, tzinfo=utc), verbose_name='date uploaded'),
        ),
    ]