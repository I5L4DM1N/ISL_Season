# Generated by Django 2.0.3 on 2018-05-31 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0009_auto_20180531_1227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generalplayer',
            old_name='PlayerName',
            new_name='Name',
        ),
    ]
