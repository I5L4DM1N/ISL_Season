# Generated by Django 2.0.3 on 2018-09-13 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0036_auto_20180705_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='daytable',
            name='EndofDay',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='daytable',
            name='EndofWeek',
            field=models.BooleanField(default=False),
        ),
    ]
