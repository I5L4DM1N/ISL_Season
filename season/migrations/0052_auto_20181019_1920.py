# Generated by Django 2.0.3 on 2018-10-19 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0051_playerfitnesslog_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerfitnesslog',
            name='Name',
        ),
        migrations.RemoveField(
            model_name='playerfitnesslog',
            name='Team',
        ),
    ]
