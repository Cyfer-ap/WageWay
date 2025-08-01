# Generated by Django 5.1.7 on 2025-06-17 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_booking_agreed_booking_issue_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='customer_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='provider_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
