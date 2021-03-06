# Generated by Django 2.0.3 on 2018-06-09 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0022_auto_20180608_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameteamlog',
            name='AttackValue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameteamlog',
            name='DefenseValue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameteamlog',
            name='Intensity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gameteamlog',
            name='Status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='gameteamlog',
            name='StatusChange',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
