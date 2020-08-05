# Generated by Django 3.0.8 on 2020-08-05 08:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0016_auto_20200805_0836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='essay',
            old_name='words',
            new_name='characters',
        ),
        migrations.AddField(
            model_name='essay',
            name='essay_text',
            field=models.TextField(default='hej max hej max hej max', max_length=200000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='essay',
            name='upload_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 5, 8, 53, 27, 627192, tzinfo=utc), verbose_name='date uploaded'),
        ),
    ]
