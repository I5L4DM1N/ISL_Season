# Generated by Django 2.0.3 on 2018-06-02 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0018_remove_playermotivationlog_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermotivationlog',
            name='MotivationChange',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
