# Generated by Django 4.2.5 on 2024-04-17 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_booking_number_of_adult_booking_number_of_children'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='number_of_adult',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='number_of_children',
        ),
    ]
