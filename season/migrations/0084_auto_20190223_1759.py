# Generated by Django 2.0.3 on 2019-02-23 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0083_auto_20190223_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayerlog',
            name='MaxAttackPerformance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='MaxDefencePerformance',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
