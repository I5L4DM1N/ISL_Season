# Generated by Django 2.0.3 on 2018-05-31 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('season', '0008_generalteam_logo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generalplayer',
            old_name='PlayerImage',
            new_name='Image',
        ),
    ]
