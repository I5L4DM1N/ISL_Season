# Generated by Django 2.2.1 on 2019-05-27 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0101_auto_20190527_2123'),
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
