from django.db import models
from services.models import Service
from users.models import User

BOOKING_STATUS = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
    ('rejected', 'Rejected'),
)

PROVIDER_RESPONSE = (
    ('waiting', 'Waiting for Response'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)

PAYMENT_METHODS = (
    ('upi', 'UPI'),
    ('bank_transfer', 'Bank Transfer'),
    ('cod', 'Cash on Delivery'),
    ('credit_card', 'Credit Card'),
)

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()

    # Status fields
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='pending')
    provider_response = models.CharField(max_length=10, choices=PROVIDER_RESPONSE, default='waiting')

    # Enhancements
    urgent = models.BooleanField(default=False)
    issue_description = models.TextField(blank=True)
    material_available = models.BooleanField(default=False)
    preferred_payment = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True)
    agreed = models.BooleanField(default=False)
    special_instructions = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    # Completion Confirmation
    provider_confirmed = models.BooleanField(default=False)
    customer_confirmed = models.BooleanField(default=False)

    @property
    def is_fully_completed(self):
        return self.provider_confirmed and self.customer_confirmed

    def __str__(self):
        return f"{self.service.title} for {self.customer.username} on {self.booking_date} at {self.booking_time}"

    def can_be_paid(self):
        return self.status == 'confirmed' and self.provider_response == 'accepted'


