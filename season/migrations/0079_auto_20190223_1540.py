# Generated by Django 2.0.3 on 2019-02-23 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0078_auto_20190214_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayerlog',
            name='AttackingPostionalDefensiveFactor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='AttackingPostionalOffensiveFactor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='DefendingPostionalDefensiveFactor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='DefendingPostionalOffensiveFactor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='PositionalExperience',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='TeamTactics',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
