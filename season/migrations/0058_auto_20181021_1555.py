# Generated by Django 2.0.3 on 2018-10-21 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0057_gameteamlog_eventplayer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameteamlog',
            name='EventPlayer',
        ),
        migrations.AddField(
            model_name='gameteamlog',
            name='EventPlayerAttack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='EventPlayerAttack', to='season.Player'),
        ),
        migrations.AddField(
            model_name='gameteamlog',
            name='EventPlayerDefence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='EventPlayerDefence', to='season.Player'),
        ),
    ]
