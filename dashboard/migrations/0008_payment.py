# Generated by Django 4.2.5 on 2024-05-17 04:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0007_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(default='esewa', max_length=100)),
                ('payment_date', models.DateField(default=datetime.datetime(2024, 5, 17, 4, 52, 40, 143603, tzinfo=datetime.timezone.utc))),
                ('amount', models.FloatField()),
                ('transaction_uuid', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
