# Generated by Django 2.0.3 on 2018-06-02 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0016_auto_20180602_2149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generalplayer',
            old_name='PlayerChemestry',
            new_name='PlayerChemistry',
        ),
    ]
