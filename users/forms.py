from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import CustomerProfile, ProviderProfile
from django.forms import ModelForm


class CustomerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        if commit:
            user.save()
        return user

class ProviderSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'provider'
        if commit:
            user.save()
        return user



class CustomerProfileForm(ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address', 'avatar', 'bio', 'facebook', 'linkedin']


class ProviderProfileForm(ModelForm):
    class Meta:
        model = ProviderProfile
        fields = [
            'phone', 'address', 'avatar', 'service_type', 'services_offered',
            'hourly_rate', 'availability', 'experience_years', 'description',
            'certification', 'facebook', 'linkedin'
        ]

