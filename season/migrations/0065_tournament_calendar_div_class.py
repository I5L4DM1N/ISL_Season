# Generated by Django 2.0.3 on 2018-12-18 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0064_remove_tournament_calendar_datatoggle'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='calendar_div_class',
            field=models.CharField(default='collapse', max_length=100),
            preserve_default=False,
        ),
    ]
