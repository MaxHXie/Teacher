# Generated by Django 3.0.8 on 2020-08-05 08:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0014_auto_20200805_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essay',
            name='upload_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 5, 8, 34, 32, 451312, tzinfo=utc), verbose_name='date uploaded'),
        ),
    ]
