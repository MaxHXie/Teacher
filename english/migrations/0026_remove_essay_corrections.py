# Generated by Django 3.0.8 on 2020-10-25 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0025_auto_20201025_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essay',
            name='corrections',
        ),
    ]
