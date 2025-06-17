from django.db import models
from users.models import User

PREFERRED_PAYMENT_CHOICES = [
    ('upi', 'UPI'),
    ('bank_transfer', 'Bank Transfer'),
    ('cash', 'Cash on Service'),
    ('other', 'Other'),
]

class JobPost(models.Model):
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('cleaning', 'Cleaning'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    payment = models.DecimalField(max_digits=8, decimal_places=2)
    preferred_payment = models.CharField(
        max_length=20, choices=PREFERRED_PAYMENT_CHOICES, default='upi'
    )
    date_needed = models.DateField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    is_assigned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.posted_by.username}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    message = models.TextField()
    expected_rate = models.DecimalField(max_digits=8, decimal_places=2)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} applied to {self.job.title}"
