# Generated by Django 3.0.8 on 2020-08-02 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0002_auto_20200802_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essay',
            name='paid',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='essay',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
