from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomerSignUpForm, ProviderSignUpForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


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

