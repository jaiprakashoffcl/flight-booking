# Generated by Django 4.1.4 on 2023-04-23 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_travel_passenger_pnr_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travel_passenger',
            name='user',
        ),
    ]
