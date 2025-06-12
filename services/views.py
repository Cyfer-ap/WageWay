from django.shortcuts import render, redirect, get_object_or_404
from .models import Service
from .forms import ServiceForm
from django.contrib.auth.decorators import login_required
from users.models import ProviderProfile

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
            service.save()
            return redirect('provider_services')
    else:
        form = ServiceForm()
    return render(request, 'services/service_form.html', {'form': form})

@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user.providerprofile)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=service)
    if form.is_valid():
        form.save()
        return redirect('provider_services')
    return render(request, 'services/service_form.html', {'form': form})

@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user.providerprofile)
    if request.method == 'POST':
        service.delete()
        return redirect('provider_services')
    return render(request, 'services/service_confirm_delete.html', {'service': service})


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

