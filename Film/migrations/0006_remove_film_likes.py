# Generated by Django 5.0.1 on 2024-02-23 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Film', '0005_film_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='likes',
        ),
    ]
