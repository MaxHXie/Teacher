# Generated by Django 3.0.8 on 2020-10-25 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0023_auto_20201025_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essay',
            name='essay_correction_string',
            field=models.TextField(default='', max_length=500000),
        ),
    ]
