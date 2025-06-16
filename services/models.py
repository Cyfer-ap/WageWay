from django.db import models
from users.models import ProviderProfile
from multiselectfield import MultiSelectField

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

PAYMENT_METHODS = (
    ('upi', 'UPI'),
    ('bank_transfer', 'Bank Transfer'),
    ('cod', 'Cash on Delivery'),
    ('credit_card', 'Credit Card'),
)

CANCELLATION_POLICIES = (
    ('anytime', 'Anytime'),
    ('before_24h', 'Before 24 Hours'),
    ('before_12h', 'Before 12 Hours'),
)

JOB_TYPES = (
    ('one_time', 'One-Time'),
    ('recurring', 'Recurring'),
)

class Service(models.Model):
    # 🧾 Basic Info
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    custom_category = models.CharField(max_length=50, blank=True)  # Used when category is "Other"
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='services')

    # 🌍 Job Type & Availability
    job_type = models.CharField(max_length=15, choices=JOB_TYPES, default='one_time')
    job_date = models.DateField(blank=True, null=True)  # One-time only
    available_days = MultiSelectField(choices=DAYS_OF_WEEK, blank=True)  # Recurring only
    from_time = models.TimeField(blank=True, null=True)
    to_time = models.TimeField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True)  # e.g. "1 hour"

    # 💰 Pricing & Payment
    rate_type = models.CharField(max_length=10, choices=RATE_TYPE_CHOICES)
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    accepted_payments = MultiSelectField(choices=PAYMENT_METHODS, blank=True)

    # 🔧 Requirements
    requirements = models.TextField(blank=True)

    # 🌍 Location (with validation logic to be added)
    service_area = models.CharField(max_length=150)
    verified_location = models.CharField(max_length=100, blank=True)  # post + district + state

    # ☎ Contact Info
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()

    # 📅 Cancellation Policy
    cancellation_policy = models.CharField(max_length=20, choices=CANCELLATION_POLICIES, default='anytime')

    # 📷 Media
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    certification = models.FileField(upload_to='certifications/', blank=True, null=True)

    # 🔐 Status & Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def display_category(self):
        return self.custom_category if self.category == 'Other' else self.category

    def get_available_days_display(self):
        day_dict = dict(self._meta.get_field('available_days').choices)
        return ', '.join(day_dict[day] for day in self.available_days)

    def get_accepted_payments_display(self):
        payment_dict = dict(self._meta.get_field('accepted_payments').choices)
        return ', '.join(payment_dict[method] for method in self.accepted_payments)

    def __str__(self):
        return f"{self.title} - {self.provider.user.username}"
