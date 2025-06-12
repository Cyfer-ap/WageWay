from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('provider', 'Provider'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    def is_provider(self):
        return self.role == 'provider'

    def is_customer(self):
        return self.role == 'customer'


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return f"Customer Profile: {self.user.username}"


class ProviderProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    service_type = models.CharField(max_length=50, blank=True)
    services_offered = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    availability = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    certification = models.FileField(upload_to='certs/', blank=True, null=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return f"Provider Profile: {self.user.username}"



