from django import forms
from .models import Service, CATEGORY_CHOICES, JOB_TYPES, PAYMENT_METHODS, CANCELLATION_POLICIES, DAYS_OF_WEEK
from django.core.exceptions import ValidationError
import datetime


class ServiceForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)
    custom_category = forms.CharField(required=False, label="Other Category")
    job_type = forms.ChoiceField(choices=JOB_TYPES, widget=forms.RadioSelect)

    job_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    available_days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    from_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    to_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))

    accepted_payments = forms.MultipleChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    requirements = forms.CharField(widget=forms.Textarea, required=False)
    contact_phone = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    cancellation_policy = forms.ChoiceField(choices=CANCELLATION_POLICIES)

    class Meta:
        model = Service
        exclude = ['provider', 'created_at', 'updated_at', 'verified_location', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        custom_category = cleaned_data.get('custom_category')
        job_type = cleaned_data.get('job_type')
        job_date = cleaned_data.get('job_date')
        available_days = cleaned_data.get('available_days')
        from_time = cleaned_data.get('from_time')
        to_time = cleaned_data.get('to_time')

        # Validate category: if "Other" then custom_category must be filled
        if category == 'Other' and not custom_category:
            self.add_error('custom_category', "Please specify a custom category.")

        # Validate time logic
        if from_time and to_time and from_time >= to_time:
            self.add_error('to_time', "End time must be after start time.")

        # Validate job type-specific fields
        if job_type == 'one_time':
            if not job_date:
                self.add_error('job_date', "Please select a date for one-time job.")
        elif job_type == 'recurring':
            if not available_days:
                self.add_error('available_days', "Select at least one day for recurring job.")
