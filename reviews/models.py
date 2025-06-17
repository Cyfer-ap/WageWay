from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from bookings.models import Booking
from users.models import User
from jobboard.models import JobPost

class Review(models.Model):
    REVIEW_TYPE_CHOICES = [
        ('poster_to_worker', 'Job Poster to Worker'),
        ('worker_to_poster', 'Worker to Job Poster'),
    ]

    # Core fields
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='reviews')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPE_CHOICES)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Poster to Worker
    timeliness = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    quality_of_work = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication_worker = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    professionalism = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    recommend_worker = models.BooleanField(blank=True, null=True)

    # Worker to Poster
    clarity_of_instructions = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    communication_poster = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    fairness_in_payment = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    respect_behavior = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    work_again = models.BooleanField(blank=True, null=True)

    class Meta:
        unique_together = (
            ('reviewer', 'job', 'review_type'),
            ('reviewer', 'booking', 'review_type'),
        )
    def __str__(self):
        return f"{self.reviewer.username} reviewed {self.reviewed_user.username} ({self.review_type}) - {self.rating}⭐"
