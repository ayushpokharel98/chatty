# Generated by Django 5.0.6 on 2024-05-23 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_profile_id_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friends',
            name='accepted',
        ),
        migrations.RemoveField(
            model_name='friends',
            name='note',
        ),
    ]
