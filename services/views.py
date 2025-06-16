from django.shortcuts import render, redirect, get_object_or_404
from .models import Service
from .forms import ServiceForm
from django.contrib.auth.decorators import login_required

# 📌 Dummy location verification function (you can replace with real API later)
def verify_location(address_text):
    # Mock logic – In real case, use Google Maps API or Indian Postal API
    # Example return: ("Rajgarh", "Mirzapur", "Uttar Pradesh")
    return "Rajgarh", "Mirzapur", "Uttar Pradesh"

@login_required
def service_list_provider(request):
    provider_profile = request.user.providerprofile
    services = Service.objects.filter(provider=provider_profile)
    return render(request, 'services/provider_service_list.html', {'services': services})

@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user.providerprofile

            # Handle custom category
            if form.cleaned_data['category'] == 'Other':
                service.category = 'Other'
                service.custom_category = form.cleaned_data['custom_category']
            else:
                service.custom_category = ''

            # Verify location
            service_area = form.cleaned_data['service_area']
            post, district, state = verify_location(service_area)
            service.verified_location = f"{post}, {district}, {state}"

            service.save()
            form.save_m2m()
            return redirect('provider_services')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})

@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user.providerprofile)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save(commit=False)

            if form.cleaned_data['category'] == 'Other':
                service.category = 'Other'
                service.custom_category = form.cleaned_data['custom_category']
            else:
                service.custom_category = ''

            # Re-verify location
            service_area = form.cleaned_data['service_area']
            post, district, state = verify_location(service_area)
            service.verified_location = f"{post}, {district}, {state}"

            service.save()
            form.save_m2m()
            return redirect('provider_services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'services/service_form.html', {'form': form})

@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user.providerprofile)
    if request.method == 'POST':
        service.delete()
        return redirect('provider_services')
    return render(request, 'services/service_confirm_delete.html', {'service': service})


# Customer-facing views remain unchanged
from django.db.models import Q

def service_list_customer(request):
    query = request.GET.get('q')
    services = Service.objects.filter(is_active=True)
    if query:
        services = services.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(service_area__icontains=query)
        )
    return render(request, 'services/service_browse.html', {'services': services})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    return render(request, 'services/service_detail.html', {'service': service})
