from django import forms
from .models import JobPost
from datetime import date
from .models import JobApplication


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            'title', 'description', 'category', 'location',
            'duration', 'payment', 'preferred_payment', 'date_needed'
        ]
        widgets = {
            'date_needed': forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_date_needed(self):
        d = self.cleaned_data['date_needed']
        if d < date.today():
            raise forms.ValidationError("Date needed cannot be in the past.")
        return d

    def clean_payment(self):
        p = self.cleaned_data['payment']
        if p <= 0:
            raise forms.ValidationError("Payment must be a positive value.")
        return p



class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['message', 'expected_rate', 'resume']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_expected_rate(self):
        rate = self.cleaned_data['expected_rate']
        if rate <= 0:
            raise forms.ValidationError("Expected rate must be a positive number.")
        return rate
