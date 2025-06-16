from django import forms
from .models import Booking, PAYMENT_METHODS
from datetime import date, datetime, time

class BookingForm(forms.ModelForm):
    urgent = forms.BooleanField(required=False, label="Is this urgent?")
    material_available = forms.BooleanField(required=False, label="Do you have the required materials?")
    agreed = forms.BooleanField(required=True, label="I agree to the Terms and Cancellation Policy")

    booking_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Preferred Date"
    )

    booking_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Preferred Time"
    )

    preferred_payment = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect,
        label="Preferred Payment Method"
    )

    issue_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Describe the issue for the provider'}),
        label="Describe the issue"
    )

    special_instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Any special instructions'}),
        label="Special Instructions"
    )

    class Meta:
        model = Booking
        fields = [
            'booking_date', 'booking_time', 'urgent', 'issue_description',
            'material_available', 'preferred_payment', 'agreed', 'special_instructions'
        ]

    def clean_booking_date(self):
        booking_date = self.cleaned_data['booking_date']
        if booking_date < date.today():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        booking_time = cleaned_data.get('booking_time')
        if booking_time and booking_time < time(6, 0):
            self.add_error('booking_time', "Bookings must be after 6:00 AM.")
