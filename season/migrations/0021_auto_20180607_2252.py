# Generated by Django 2.0.3 on 2018-06-07 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0020_auto_20180606_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameteamlog',
            name='MotivationChange',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
