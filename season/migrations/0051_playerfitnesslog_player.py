# Generated by Django 2.0.3 on 2018-10-19 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0050_gameplayerlog_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerfitnesslog',
            name='Player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='season.Player'),
        ),
    ]
