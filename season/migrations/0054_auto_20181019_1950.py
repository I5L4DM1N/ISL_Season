# Generated by Django 2.0.3 on 2018-10-19 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0053_auto_20181019_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempmotivationlog',
            name='Name',
        ),
        migrations.RemoveField(
            model_name='tempmotivationlog',
            name='Team',
        ),
    ]
