# Generated by Django 2.0.3 on 2019-02-23 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0086_auto_20190224_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayerlog',
            name='SentOffDefAbilityChange',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameplayerlog',
            name='SentOffOffAbilityChange',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
