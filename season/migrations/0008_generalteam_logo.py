# Generated by Django 2.0.3 on 2018-05-31 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0007_generalplayer_playerimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalteam',
            name='Logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
