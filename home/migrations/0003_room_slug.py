# Generated by Django 5.0.1 on 2024-03-21 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_rename_name_room_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='slug',
            field=models.CharField(default='', max_length=20),
        ),
    ]
