# Generated by Django 5.0.6 on 2024-05-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default_avatar.png', upload_to='profile_picture'),
        ),
    ]
