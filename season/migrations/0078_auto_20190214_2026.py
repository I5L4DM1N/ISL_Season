# Generated by Django 2.0.3 on 2019-02-14 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0077_gameplayerlog_matchrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='FanClub',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='FanClubDescription',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='FullName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='Stadium',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='StadiumDescription',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
