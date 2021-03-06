# Generated by Django 2.0.3 on 2019-03-23 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0088_auto_20190224_0035'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayerlog',
            name='AttackAbilityChangeEffect',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='AttackAbilityChangePerformance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='DefenceAbilityChangeEffect',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='DefeneceAbilityChangePerformance',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
