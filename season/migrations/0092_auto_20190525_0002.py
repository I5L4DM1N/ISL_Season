# Generated by Django 2.2.1 on 2019-05-24 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0091_auto_20190524_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalschedule',
            name='AwayTeam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AwayTeam', to='season.Team'),
        ),
        migrations.AddField(
            model_name='generalschedule',
            name='HomeTeam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='HomeTeam', to='season.Team'),
        ),
    ]
