from django.db import models
from users.models import ProviderProfile

CATEGORY_CHOICES = (
    ('Cleaning', 'Cleaning'),
    ('Electrical', 'Electrical'),
    ('Plumbing', 'Plumbing'),
    ('Carpentry', 'Carpentry'),
    ('Tutoring', 'Tutoring'),
    ('Other', 'Other'),
)

RATE_TYPE_CHOICES = (
    ('hourly', 'Hourly'),
    ('fixed', 'Fixed'),
    ('per_job', 'Per Job'),
)

DAYS_OF_WEEK = (
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
)

class Service(models.Model):
    # 🧾 Basic Info
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='services')

    # 🌍 Service Area & Availability
    service_area = models.CharField(max_length=100)
    available_days = models.CharField(max_length=100)  # e.g. comma-separated "mon,tue,wed"
    availability_time = models.CharField(max_length=100)  # e.g. "10:00 AM - 6:00 PM"
    duration = models.CharField(max_length=50)  # e.g. "1 hour"

    # 💰 Pricing
    rate_type = models.CharField(max_length=10, choices=RATE_TYPE_CHOICES)
    rate = models.DecimalField(max_digits=8, decimal_places=2)

    # 📷 Media
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    certification = models.FileField(upload_to='certifications/', blank=True, null=True)

    # 🔐 Status & Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.provider.user.username}"
