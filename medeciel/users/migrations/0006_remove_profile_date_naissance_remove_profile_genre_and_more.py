# Generated by Django 5.1.7 on 2025-03-14 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='date_naissance',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='user',
            name='full_name',
        ),
    ]
