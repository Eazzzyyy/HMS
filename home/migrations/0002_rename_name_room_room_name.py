# Generated by Django 5.0.1 on 2024-03-20 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='name',
            new_name='room_name',
        ),
    ]
