# Generated by Django 2.0.3 on 2018-10-07 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0037_auto_20180913_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerfitnesslog',
            name='Fitness',
        ),
        migrations.AddField(
            model_name='playerfitnesslog',
            name='NewFitness',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playerfitnesslog',
            name='OldFitness',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='playerfitnesslog',
            name='Team',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
