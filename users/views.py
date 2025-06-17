from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomerSignUpForm, ProviderSignUpForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import CustomerProfileForm, ProviderProfileForm
from emails.utils import send_dynamic_email


def home(request):
    return render(request, 'home.html')


@csrf_exempt
@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')


@csrf_exempt
@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('provider_dashboard')
    return render(request, 'users/customer_dashboard.html')


@csrf_exempt
@login_required
def provider_dashboard(request):
    if request.user.role != 'provider':
        return redirect('customer_dashboard')
    return render(request, 'users/provider_dashboard.html')


@csrf_exempt
def register_customer(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            send_dynamic_email(
                subject='Welcome to Wage Way!',
                to_email=user.email,
                template_name='emails/registration_success.html',
                context={'user': user}
            )

            return redirect('dashboard')  # change this as needed
    else:
        form = CustomerSignUpForm()
    return render(request, 'users/register.html', {'form': form, 'role': 'Customer'})


@csrf_exempt
def register_provider(request):
    if request.method == 'POST':
        form = ProviderSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            send_dynamic_email(
                subject='Welcome to Wage Way!',
                to_email=user.email,
                template_name='emails/registration_success.html',
                context={'user': user}
            )

            return redirect('dashboard')  # change this as needed
    else:
        form = ProviderSignUpForm()
    return render(request, 'users/register.html', {'form': form, 'role': 'Provider'})


@method_decorator(csrf_exempt, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        if self.request.user.role == 'customer':
            return '/dashboard/customer/'
        elif self.request.user.role == 'provider':
            return '/dashboard/provider/'
        else:
            return '/'


@login_required
def customer_profile(request):
    profile = request.user.customerprofile
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = CustomerProfileForm(instance=profile)
    return render(request, 'users/customer_profile.html', {'form': form})


@login_required
def provider_profile(request):
    profile = request.user.providerprofile
    if request.method == 'POST':
        form = ProviderProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProviderProfileForm(instance=profile)
    return render(request, 'users/provider_profile.html', {'form': form})


def public_provider_profile(request):
    user_id = request.GET.get('id')
    user = get_object_or_404(User, id=user_id, role='provider')
    profile = getattr(user, 'providerprofile', None)
    if not profile:
        return render(request, 'users/provider_not_found.html', {'user': user})
    return render(request, 'users/public_provider_profile.html', {
        'user': user,
        'profile': profile
    })

