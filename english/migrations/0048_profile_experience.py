# Generated by Django 3.0.8 on 2021-02-04 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0047_essay_upvotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='experience',
            field=models.IntegerField(default=0),
        ),
    ]
